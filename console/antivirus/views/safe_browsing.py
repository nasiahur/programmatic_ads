#
#
#
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from _domain.core import Build
from _domain.antivirus import WsGsbLog, WsGsbStatus

#
#
#
from antivirus.models import SafeBrowsing

from django import forms
#
#
#

class SafeBrowsingForm(forms.ModelForm):

    class Meta:

        model  = SafeBrowsing
        fields = ['enable', 'deny_url', 'api_key', 'check_malware', 'check_social', 'check_unwanted_soft', 'cache_clean', 'daemon_port']

    def clean_deny_url(self):

        value = self.cleaned_data['deny_url']
        value = value.strip().lower()

        if not (value.startswith("http://") or value.startswith("https://")):
            raise forms.ValidationError("Deny URL must start with http:// or https:// instead of %s." % value)

        return value



class ViewSafeBrowsingEdit(SuccessMessageMixin, generic.edit.UpdateView):

    model           = SafeBrowsing
    form_class      = SafeBrowsingForm
    success_message = "need_squid_restart"
    template_name   = "antivirus/safe_browsing/safe_browsing_form.html"

    def get_object(self):
        return SafeBrowsing.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewSafeBrowsingEdit")

    def get_context_data(self, **kwargs):

        context  = super(ViewSafeBrowsingEdit, self).get_context_data(**kwargs)
        context['version'] = Build.version()
        return context

#
#
#
class ViewSafeBrowsingHelpers(SuccessMessageMixin, generic.edit.UpdateView):

    model           = SafeBrowsing
    fields          = ['helper_verbose', 'helper_total', 'helper_idle', 'helper_startup']
    
    success_message = "need_squid_restart"
    template_name   = "antivirus/safe_browsing/helpers_form.html"

    def get_object(self):
        return SafeBrowsing.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewSafeBrowsingHelpers")


#
# 
#
class ViewSafeBrowsingLog(generic.base.TemplateView):

    template_name = "antivirus/safe_browsing/log.html"
    
    def get_context_data(self, **kwargs):

        context = super(ViewSafeBrowsingLog, self).get_context_data(**kwargs)        

        # get size, include and exclude strings from request
        include = self.request.GET.get('include', '')
        exclude = self.request.GET.get('exclude', '')
        size    = 256
        try:
            size = int(self.request.GET.get('size', '256'))
            if size > 1024:
                size = 1024
        except Exception, e:
            pass

        # save into context
        context['size']         = size
        context['include']      = include
        context['exclude']      = exclude
        context['log_contents'] = self.get_contents(size, include, exclude)
        context['log_size']     = self.get_size()
        context['log_path']     = WsGsbLog().get_path()

        return context

    def get_size(self):

        log  = WsGsbLog()
        size = log.get_size()
       
        return size

    def get_contents(self, line_count, include, exclude):

        log      = WsGsbLog()
        contents = log.get_contents(line_count, include, exclude)
        if not contents:
            contents = "Requested log file is empty."
        
        return contents


#
# 
#
class ViewSafeBrowsingStatus(generic.base.TemplateView):

    template_name = "antivirus/safe_browsing/status.html"
    
    def get_context_data(self, **kwargs):

        context = super(ViewSafeBrowsingStatus, self).get_context_data(**kwargs)

        # allocate default info
        data = {
            "Stats" : {
                "QueriesByDatabase": 0,
                "QueriesByCache":    0,
                "QueriesByAPI":      0,
                "QueriesFail":       0,
                "DatabaseUpdateLag": 0
            },
            "Error":""
        }
        
        try:
            # get the wsgsbd port for the REST service
            port = 18890

            '''            
            name = os.path.join(Paths.etc_dir(), "node", "wssyncd.json")
            with open(name) as fin:    
                wssyncd = json.load(fin)
                wsport  = wssyncd['rest_service']['port']
            '''

            data = WsGsbStatus().run(port)
            
        except Exception as e:
            data['Error'] = str(e)
        
        context['info'] = data

        return context

    def get_size(self):

        log  = self.log_class()
        size = log.get_size()
       
        return size

    def get_contents(self, line_count, include, exclude):

        log      = self.log_class()
        contents = log.get_contents(line_count, include, exclude)
        if not contents:
            contents = "Requested log file is empty."
        
        return contents
