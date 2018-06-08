import os
import os.path

#
# business logic
#
from _domain.core import Paths
from _domain.utils import FolderInfo
from _domain.traffic import ReportLog, MonitorLog, DatabaseLog

#
# django
#
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import FormMixin, FormView
from django.views.generic.detail import DetailView
from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#
#
#
from traffic.history import HistoryManager
from traffic.models import *
from traffic.forms import *
from console.settings import DATABASES
from traffic.manager import ReportManager
from traffic.pdf.pdf_generator import generate_pdf_report, valid_pdf_install

#
# reports
#
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

#
#
#
class ViewReportTemplates(generic.TemplateView):
    template_name = 'traffic/report/template_list.html'

#
# jobs
#
class ViewReportJobs(SuccessMessageMixin, generic.ListView):

    template_name = 'traffic/report/job_list.html'
    model = Job

    def get_queryset(self):
        return Job.objects.order_by('template_type')

    def post(self, request, *args, **kwargs):

        # drop all items of that model by primary key
        for selected_id in request.POST.getlist('selected_id'):
            item = get_object_or_404(Job, pk = selected_id)

            item.remove_generated_dir()
            item.delete()

        # tell the user squid needs to be reloaded or restarted
        messages.info(self.request, "need_squid_restart")

        # and redirect to success url
        return HttpResponseRedirect(reverse_lazy('traffic:ViewReportJobs'))

    def get_context_data(self, **kwargs):
        context  = super(ViewReportJobs, self).get_context_data(**kwargs)

        domains    = []
        bandwidth  = []
        users      = []
        categories = []
        policies   = []

        for item in Job.objects.all():
            if item.template_type.startswith('icap-domains'):
                domains.append(item)
            elif item.template_type.startswith('icap-requests') or item.template_type.startswith('icap-bandwidth'):
                bandwidth.append(item)
            elif item.template_type.startswith('icap-users'):
                users.append(item)
            elif item.template_type.startswith('icap-categories'):
                categories.append(item)
            elif item.template_type.startswith('icap-policies'):
                policies.append(item)

        context['domains']    =  domains
        context['bandwidth']  =  bandwidth
        context['users']      =  users
        context['categories'] =  categories
        context['policies']   =  policies

        return context


class ViewReportCreateJob(SuccessMessageMixin, generic.edit.CreateView):

    model           = Job
    form_class      = JobForm
    success_message = "need_squid_restart"
    template_name   = 'traffic/report/job_form.html'

    def get_context_data(self, **kwargs):
        context = super(ViewReportCreateJob, self).get_context_data(**kwargs)
        context['type']        = self.kwargs['template']

        # various flags
        #context['show_limits'] = self.show_limits(self.kwargs['template'])
        #context['show_limits_domains'] = self.show_limits_domains(self.kwargs['template'])
        return context

    '''
    def show_limits(self, template_name):
        if self.show_limits_domains(template_name):
            return True
        return False

    def show_limits_domains(self, template_name):

        if template_name in [
            "icap-domains-detailed",
            "icap-users-detailed-by-domains",
            "icap-users-detailed-unproductive-by-domains",
            "icap-users-detailed-blocked-by-domains",
            "icap-dates-detailed-by-bandwidth",
            "icap-hours-detailed-by-bandwidth",
            "icap-categories-detailed"
        ]:
            return True
        return False
    '''

    def get_success_url(self):
        return reverse_lazy('traffic:ViewReportJobs')


class ViewReportUpdateJob(SuccessMessageMixin, generic.edit.UpdateView):

    model = Job
    form_class = JobForm
    success_message = "need_squid_restart"
    template_name   = 'traffic/report/job_form.html'

    def get_context_data(self, **kwargs):
        context = super(ViewReportUpdateJob, self).get_context_data(**kwargs)
        context['reporter'] = Reporter.objects.first()
        context['type']     = self.kwargs['template']
        return context

    def get_success_url(self):
        return reverse_lazy('traffic:ViewReportJobs')


class ViewReportGenerateJob(generic.View):

    def get(self, request, *args, **kwargs):

        # get reporter
        r = Reporter.objects.first()

        # get the corresponding job
        j = r.job_set.filter(id=self.kwargs['pk'])
        if len(j) != 1:
            raise Exception("Cannot get job by id")

        # this is the job to run
        job = j[0]

        # call the report manager telling him to run the job
        res = ReportManager().create_report(job.name)
        if res['success'] != True:
            messages.info(self.request, "cannot generate job '%s', error: %s" % (job.name, res['error']))

        # and redirect to success url
        return HttpResponseRedirect(reverse_lazy('traffic:ViewReportList'))


class ViewReportViewJob(generic.View):

    def get(self, request, *args, **kwargs):

        job_name = self.kwargs["name"]
        job_file = self.kwargs["file"]

        fullname = os.path.join(Paths.var_dir(), "reports", job_name, job_file)
        data     = None
        try:
            with open (fullname, "r") as fin:
                data = fin.read()
        except Exception, e:
            raise

        mimetype = "text/html"
        if job_file.endswith(".json"):
            mimetype = "application/json"
        elif job_file.endswith(".css"):
            mimetype = "text/css"
        elif job_file.endswith(".log"):
            mimetype = "text/plain"

        return HttpResponse(data, content_type=mimetype)

class ViewReportExportPdf(generic.View):
    help = "Please contact support at support@diladele.com"

    def send_pdf_report(self, directory, job_name):
        fullname = os.path.join(directory, "data", "report.pdf")
        data     = None
        try:
            with open (fullname, "r") as fin:
                data = fin.read()
        except Exception as e:
            return HttpResponse("Could not open pdf report: '%s'.\n%s" % (str(e), self.help), content_type="text/plain")

        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "attachment; filename=\"%s.pdf\"" % job_name
        
        return response

    def send_pdf_log(self, directory):

        fullname = os.path.join(directory, "data", "pdf.log")
        data     = None
        try:
            with open (fullname, "r") as fin:
                data = fin.read()
        except Exception as e:
            return HttpResponse("Could not open pdf log: '%s'.\n%s" %(str(e), self.help), content_type="text/plain")

        return HttpResponse(data + self.help, content_type="text/plain")

    def get(self, request, *args, **kwargs):

        job_name = self.kwargs["name"]
        
        if not valid_pdf_install():
            return HttpResponse(
                "<body><h2>ReportLab is not installed</h2><p>Please visit <a href=\"https://docs.diladele.com/\">https://docs.diladele.com</a> " +
                "for installation instructions (for example for " + 
                "<a href='https://docs.diladele.com/administrator_guide_6_1/install/ubuntu16/apache.html'>Ubuntu 16 LTS</a>).</p></body>", 
                content_type="text/html"
            )
        
        directory = os.path.join(Paths.var_dir(), "reports", job_name)
        pdfFile   = os.path.join(directory, "data", "report.pdf")
        if os.path.isfile(pdfFile):
            return self.send_pdf_report(directory, job_name)
        else:
            return self.send_pdf_log(directory)



####################################################################################################
#
# MONITORING
#
####################################################################################################
class MonitoringFormGlobals(forms.ModelForm):
    class Meta:
        model  = Monitoring
        fields = ['update_interval', 'history_normalize_names', 'history_anonymize_names']
        widgets = {
            'update_interval' : forms.TextInput(attrs={'style':'width: 50px'}),
        }

    def clean_update_interval(self):
        value = self.cleaned_data['update_interval']
        if value < 1:
            raise forms.ValidationError("Must be >= 1 second; recommended value is 5.")
        return value

class MonitoringFormChannels(forms.ModelForm):
    class Meta:
        model   = Monitoring        
        fields = [
            'persistent_enable', 
            'persistent_purge',
            'persistent_store_query',
            'persistent_store_path',
            'persistent_store_clean',
            'persistent_store_adblock',
            'persistent_store_privacy',
            'persistent_store_adult_heuristics',
            'persistent_store_adult_safesearch',
            'persistent_store_adult_youtube',
            'persistent_store_adult_phrases',
            'persistent_store_adult_image',
            'persistent_store_categories',
            'persistent_store_http_sanitation',
            'persistent_store_content_content_type',
            'persistent_store_content_charset',
            'persistent_store_content_transfer_encoding',
            'persistent_store_content_file_name',
            'persistent_store_content_file_type',
            'persistent_store_content_file_size',
            'persistent_store_apps',
            'persistent_store_sslbump',
            'realtime_enable',
            'realtime_store_query',
            'realtime_store_path',
            'realtime_store_clean',
            'realtime_store_adblock',
            'realtime_store_privacy',
            'realtime_store_adult_heuristics',
            'realtime_store_adult_safesearch', 
            'realtime_store_adult_youtube',
            'realtime_store_adult_phrases',
            'realtime_store_adult_image', 
            'realtime_store_categories',
            'realtime_store_http_sanitation', 
            'realtime_store_content_content_type',
            'realtime_store_content_charset', 
            'realtime_store_content_transfer_encoding',
            'realtime_store_content_file_name', 
            'realtime_store_content_file_type',
            'realtime_store_content_file_size', 
            'realtime_store_apps',
            'realtime_store_sslbump', 
            'realtime_limit_record_count',
            'accesslog_enable',
            'accesslog_store_query',
            'accesslog_store_path',
            'accesslog_store_clean',
            'accesslog_store_adblock',
            'accesslog_store_privacy',
            'accesslog_store_adult_heuristics', 
            'accesslog_store_adult_safesearch',
            'accesslog_store_adult_youtube',
            'accesslog_store_adult_phrases',
            'accesslog_store_adult_image',
            'accesslog_store_categories', 
            'accesslog_store_http_sanitation',
            'accesslog_store_content_content_type', 
            'accesslog_store_content_charset',
            'accesslog_store_content_transfer_encoding',
            'accesslog_store_content_file_name',
            'accesslog_store_content_file_type', 
            'accesslog_store_content_file_name',
            'accesslog_store_content_file_type',
            'accesslog_store_content_file_size',
            'accesslog_store_apps',
            'accesslog_store_sslbump',
            'syslog_enable',
            'syslog_store_query',
            'syslog_store_path',
            'syslog_store_clean',
            'syslog_store_adblock',
            'syslog_store_privacy',
            'syslog_store_adult_heuristics',
            'syslog_store_adult_safesearch',
            'syslog_store_adult_youtube',
            'syslog_store_adult_phrases', 
            'syslog_store_adult_image',
            'syslog_store_categories',
            'syslog_store_http_sanitation', 
            'syslog_store_content_content_type',
            'syslog_store_content_charset',
            'syslog_store_content_transfer_encoding', 
            'syslog_store_content_file_name',
            'syslog_store_content_file_type',
            'syslog_store_content_file_size', 
            'syslog_store_apps',
            'syslog_store_sslbump'
        ]

        widgets = {
            'realtime_limit_size_mb' : forms.TextInput(attrs={'style':'width: 50px'}),
            'realtime_limit_time_min' : forms.TextInput(attrs={'style':'width: 50px'}),
            'realtime_limit_record_count' : forms.TextInput(attrs={'style':'width: 50px'}),
            'persistent_purge'   : forms.TextInput(attrs={'style':'width: 50px'}),
        }

    def clean_realtime_limit_size_mb(self):
        value = self.cleaned_data['realtime_limit_size_mb']
        if value > 1024 or value < 1:
            raise forms.ValidationError("Must be within [1:1024] interval; recommended value is 50.")
        return value

    def clean_realtime_limit_time_min(self):
        value = self.cleaned_data['realtime_limit_time_min']
        if value > 60 or value < 1:
            raise forms.ValidationError("Must be within [1:60] interval; recommended value is 5.")
        return value

    def clean_persistent_purge(self):
        value = self.cleaned_data['persistent_purge']
        if value < 1:
            raise forms.ValidationError("Must be >= 1 day")
        return value


#
#
#
class View_MonitoringUpdateGlobals(SuccessMessageMixin, generic.edit.UpdateView):
    model           = Monitoring
    form_class      = MonitoringFormGlobals
    success_message = "need_squid_restart"
    template_name   = "traffic/monitor/monitoring_form_globals.html"

    def get_object(self):
        return Monitoring.objects.first()

    def get_success_url(self):
        return reverse_lazy('traffic:View_MonitoringUpdateGlobals')

class View_MonitoringUpdateChannels(SuccessMessageMixin, generic.edit.UpdateView):
    model           = Monitoring
    form_class      = MonitoringFormChannels
    success_message = "need_squid_restart"
    template_name   = "traffic/monitor/monitoring_form_channels.html"

    def get_object(self):
        return Monitoring.objects.first()

    def get_success_url(self):
        return reverse_lazy('traffic:View_MonitoringUpdateChannels')

class ReporterSmtpConnectorForm(forms.ModelForm):
    class Meta:
        model  = Reporter
        fields = ['smtp_username', 'smtp_password', 'smtp_server', 'smtp_port', 'smtp_use_auth']

    smtp_password = forms.CharField(widget=forms.PasswordInput())

class View_MonitoringUpdateSmtpConnector(SuccessMessageMixin, generic.edit.UpdateView):
    model           = Reporter
    form_class      = ReporterSmtpConnectorForm
    success_message = "need_squid_restart"
    template_name   = "traffic/monitor/monitoring_form_smtpconnector.html"

    def get_object(self):
        return Reporter.objects.first()

    def get_success_url(self):
        return reverse_lazy('traffic:View_MonitoringUpdateSmtpConnector')


class WsMgrdForm(forms.ModelForm):
    class Meta:
        model  = WsMgrd
        fields = ['logging']

class View_MonitoringUpdateAdvanced(SuccessMessageMixin, generic.edit.UpdateView):
    model           = WsMgrd
    form_class      = WsMgrdForm
    success_message = "need_squid_restart"
    template_name   = "traffic/monitor/monitoring_form_advanced.html"

    def get_object(self):
        return WsMgrd.objects.first()

    def get_success_url(self):
        return reverse_lazy('traffic:View_MonitoringUpdateAdvanced')

#
#
#
class BrowsingHistoryForm(forms.Form):
    column_name = forms.ChoiceField(
        required = False,
        choices  = BrowsingHistory.COLUMN_NAME_CHOICES,
        widget   = forms.Select(
            attrs={'class':'span2'}
        )
    )

    column_value = forms.CharField(max_length=50, required=False,
        widget=forms.TextInput(
            attrs={'class':'span8', 'placeholder':'Type here column expected value to filter records'}
        )
    )

    def clean(self):
        cleaned_data = super(BrowsingHistoryForm, self).clean()
        name = cleaned_data.get('column_name')
        value = cleaned_data.get('column_value')

        if name == '':
            cleaned_data['column_name'] = 0
            return cleaned_data
        else:
            name = int(name)

        if name == BrowsingHistory.COLUMN_NAME_INCIDENT and not value.isdigit():
            raise forms.ValidationError("Error: Incident value should be a positive number. All objects returned.")
        return cleaned_data

class FormListView(FormMixin, generic.ListView):
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

class View_MonitorIncidentList(FormListView):
    form_class = BrowsingHistoryForm
    model = Event
    paginate_by = 100
    template_name = 'traffic/monitor/event_list.html'

    def get_queryset(self):
        self.form = BrowsingHistoryForm(self.request.GET)

        name = self.request.GET.get('cn')
        value = self.request.GET.get('cv')

        if name and name.isdigit():
            self.column_name = int(name)
            self.column_value = value
        elif self.form.is_valid():
            self.column_name = int(self.form.cleaned_data['column_name'])
            self.column_value = self.form.cleaned_data['column_value']
        else:
            self.column_name = BrowsingHistory.COLUMN_NAME_NONE
            self.column_value = ""

        if self.column_name == 0:
            return Event.objects.all().order_by('-timestamp', '-iid')[:1000]

        db_filter = BrowsingHistory.COLUMN_NAME_TO_DB_FILTER[self.column_name]
        kwargs = { '{0}'.format(db_filter): self.column_value }
        return Event.objects.filter(**kwargs).order_by('-timestamp', '-iid')[:1000]

    def get_context_data(self, **kwargs):
        context = super(View_MonitorIncidentList, self).get_context_data(**kwargs)
        context['cn'] = self.column_name
        context['cv'] = self.column_value
        return context

class View_MonitorIncident(generic.DetailView):
    model = Event
    template_name = 'traffic/monitor/event_detail.html'

class SurfingNowForm(forms.Form):
    column_name = forms.ChoiceField(
        required = False,
        choices  = SurfingNow.COLUMN_NAME_CHOICES,
        widget   = forms.Select(
            attrs={'class':'span2'}
        )
    )

    column_value = forms.CharField(max_length=50, required=False,
        widget=forms.TextInput(
            attrs={'class':'span8', 'placeholder':'Type here column expected value to filter records'}
        )
    )

    def clean(self):
        cleaned_data = super(SurfingNowForm, self).clean()
        name = cleaned_data.get('column_name')
        value = cleaned_data.get('column_value')

        if name == '':
            cleaned_data['column_name'] = 0
            return cleaned_data
        else:
            name = int(name)

        if name == SurfingNow.COLUMN_NAME_INCIDENT and not value.isdigit():
            raise forms.ValidationError("Error: Incident value should be a positive number. All objects returned.")
        return cleaned_data

class View_MonitorSurfingNow(FormListView):
    lastAsc = False

    def get(self, request, *args, **kwargs):
        order_by = request.GET.get('order_by')
        previous_order_by = request.GET.get('pob')
        name = self.request.GET.get('cn')
        value = self.request.GET.get('cv')
        asc = self.request.GET.get('asc', False)
        header_click = self.request.GET.get('reverse_asc', False)
        submitted_thru_form = request.GET.get('column_name', False)

        form = SurfingNowForm(self.request.GET)

        if name and name.isdigit():
            column_name = int(name)
            column_value = value
        elif form.is_valid():
            column_name = int(form.cleaned_data['column_name'])
            column_value = form.cleaned_data['column_value']
            order_by = "timestamp"
        else:
            column_name = SurfingNow.COLUMN_NAME_NONE
            column_value = ""
            order_by = "timestamp"

        if submitted_thru_form:
            asc = False
            order_by = "timestamp"

        if header_click:
            if order_by == previous_order_by and order_by is not None and order_by != '':
                if asc == 'True':
                    asc = False
                else:
                    asc = True
            else:
                if order_by == 'timestamp' or order_by == 'iid':
                    asc = False
                else:
                    asc = True

        previous_order_by = order_by

        object_list = HistoryManager().get_all(SurfingNow.COLUMN_NAME_TO_DB_COLUMN[column_name], column_value, order_by, 1000, asc)
        paginator = Paginator(object_list, 100)
        page = request.GET.get('page')

        try:
            items = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
        # for i in items:
        #     print(i.host)
        ctx = {
            'form':form,
            'items':items,
            'paginator' : paginator,
            'page_obj' : items,
            'cn': column_name,
            'cv': column_value,
            'order_by': order_by,
            'page': page,
            'ascending': asc,
            'pob': previous_order_by }

        return render(request, 'traffic/monitor/surfing_all.html', ctx)

class View_MonitorInfo(generic.TemplateView):
    template_name  = 'traffic/monitor/monitor_info.html'

    def get_context_data(self, **kwargs):
        context = super(View_MonitorInfo, self).get_context_data(**kwargs)

        # set if we use sqlite and how many ips we have
        is_sqlite  = (DATABASES['monitor']['ENGINE'] == 'django.db.backends.sqlite3')

        # amend context
        context['is_sqlite'] = is_sqlite
        context['db_engine'] = DATABASES['monitor']['ENGINE']
        if is_sqlite:
            context['db_size'] = os.path.getsize(DATABASES['monitor']['NAME'])
        else:
            # for mysql we ask it directly
            try:
                context['db_size'] = 0

                cursor = connection.cursor()
                cursor.execute("SELECT sum(round(((data_length + index_length) / 1024 / 1024 / 1024), 2))  as 'Size in GB' FROM information_schema.TABLES WHERE table_schema = 'websafety_monitor'")
                row = cursor.fetchone()

                # here we get error - no such table: information_schema.TABLES why???
                context['db_size'] = row[0]

            except Exception as e:
                pass

        context['upload_size'] = FolderInfo(os.path.join(Paths.var_dir(), "monitor")).get_size()
        return context

class View_MonitorUploadLog(generic.TemplateView):
    template_name = "traffic/monitor/monitor_log.html"

    def get_context_data(self, **kwargs):
        context = super(View_MonitorUploadLog, self).get_context_data(**kwargs)
        context['monitor_log'] = MonitorLog().get()
        return context

class View_MonitorDatabaseLog(generic.TemplateView):
    template_name = "traffic/monitor/database_log.html"

    def get_context_data(self, **kwargs):
        context = super(View_MonitorDatabaseLog, self).get_context_data(**kwargs)
        context['database_log'] = DatabaseLog().get()
        return context
