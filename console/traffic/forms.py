#
# system
#

#
# django
#
from django import forms

#
# our
#
from traffic.models import *

class JobForm(forms.ModelForm):

    class Meta:
        model  = Job
        fields = '__all__'
        '''
        fields = ['reporter', 'comments', 'name', 'email_report_to', 'schedule_min', 'schedule_hour', 'schedule_dom', 'schedule_month', 'schedule_dow',
            'template_type', 'timeframe_type', 'timeframe_value', 'timeframe_from', 'timeframe_to', 'include_current', 'limit_n_entries', 'limit_n_drilldown',
            'include_domains', 'include_users', 'include_ips', 'include_policies', 'include_user_activities', 'include_denied_requests', 'include_unauthenticated_requests',
            'include_top_domains', 'include_bandwidth', 'squid_log_directory'
        ]
        '''
        # 'schedule_type' - all reports are now periodic!

    timeframe_from  = forms.DateField(required=False, widget=forms.DateInput(attrs={ 'class':'datepicker' }))
    timeframe_to    = forms.DateField(required=False, widget=forms.DateInput(attrs={ 'class':'datepicker' }))
    comments = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'1', 'class':'input-block-level'}),
        required=False
    )
    email = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'1', 'class':'input-block-level'}),
        required=False
    )

    include_domains = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )
    include_users = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )
    include_ips = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )
    include_policies = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )
    include_categories = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )

    exclude_domains = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )
    exclude_users = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )
    exclude_ips = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )
    exclude_policies = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )
    exclude_categories = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'2', 'class':'input-block-level'}),
        required=False
    )

    def clean(self):

        # we need to validate schedule - it must NOT be 'all *'
        if 'schedule_min' in self.cleaned_data:
            if 'schedule_hour' in self.cleaned_data:
                if 'schedule_dom' in self.cleaned_data:
                    if 'schedule_month' in self.cleaned_data:
                        if 'schedule_dow' in self.cleaned_data:

                            # ok all schedule fields are valid, get them
                            s_min   = self.cleaned_data['schedule_min'].strip()
                            s_hour  = self.cleaned_data['schedule_hour'].strip()
                            s_dom   = self.cleaned_data['schedule_dom'].strip()
                            s_month = self.cleaned_data['schedule_month'].strip()
                            s_dow   = self.cleaned_data['schedule_dow'].strip()

                            # and check
                            if s_min in ["", "*"]:
                                if s_hour in ["", "*"]:
                                    if s_dom in ["", "*"]:
                                        if s_month in ["", "*"]:
                                            if s_dow in ["", "*"]:
                                                raise forms.ValidationError("Empty schedule is not allowed. Set at least Minutes and/or Hours")

        # validate time_type
        timeframe_type = self.cleaned_data['timeframe_type']
        if timeframe_type == PARAMETER_TIMEFRAME_FROMTO:
            timeframe_from = self.cleaned_data['timeframe_from']
            timeframe_to   = self.cleaned_data['timeframe_to']
            if timeframe_from is None or timeframe_to is None:
                raise forms.ValidationError("Please specify values for boths Date From and Date To fields")
            if timeframe_from > timeframe_to:
                raise forms.ValidationError("Date From shall be earlier that Date To field")


        return self.cleaned_data


    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)

    def clean_name(self):
        name = self.cleaned_data['name']
        if not self.is_ascii(name):
            raise forms.ValidationError("Job '%s' cannot be added, becase it contains non ASCII alphanumeric characters." % name)

        # we need to case insensitive compare names in the database, it means we must manually walk it
        for job in Job.objects.all():
            if job.pk == self.instance.pk:
                continue
            if job.name.lower() == name.lower():
                raise forms.ValidationError("Job '%s' already exists." % name)

        # check for banned symbols
        banned = ["&", "/", "\\", "(", ")", ".", ",", "*"]
        for c in banned:
            if name.find(c) != -1:
                raise forms.ValidationError("Job name cannot contain characters %s" % (" ".join(banned)))

        return name


    def clean_include_domains(self):

        value = self.cleaned_data['include_domains']
        ttype = self.cleaned_data['template_type']

        if ttype == 'icap-domains-detailed-domain-info':
            if len(value.strip()) == 0:
                raise forms.ValidationError("Domain name must be filled")

        return value

    def clean_schedule_hour(self):

        value = self.cleaned_data['schedule_hour'].strip()
        if value == '*':
            return value
        try:
            n = int(value)
            if n < 0 or n > 23:
                raise Exception("invalid hour specified (%s)" % value)
        except Exception as e:
            raise forms.ValidationError("hours must be either * or within interval [0:23]. Error: %s" % str(e))

        return value

    def clean_schedule_min(self):

        value = self.cleaned_data['schedule_min'].strip()
        if value == '*':
            return value
        try:
            n = int(value)
            if n < 0 or n > 59:
                raise Exception("invalid minute specified (%s)" % value)
        except Exception as e:
            raise forms.ValidationError("minutes must be either * or within interval [0:59]. Error: %s" % str(e))

        return value

    def clean_schedule_dom(self):

        value = self.cleaned_data['schedule_dom'].strip()
        if value == '*':
            return value
        try:
            n = int(value)
            if n < 0 or n > 31:
                raise Exception("invalid day of month specified (%s)" % value)
        except Exception as e:
            raise forms.ValidationError("Day of month must be either * or within interval [0:31]. Error: %s" % str(e))

        return value

    def clean_schedule_month(self):

        value = self.cleaned_data['schedule_month'].strip()
        if value == '*':
            return value
        try:
            n = int(value)
            if n < 1 or n > 12:
                raise Exception("invalid month specified (%s)" % value)
        except Exception as e:
            raise forms.ValidationError("Month must be either * or within interval [1:12]. Error: %s" % str(e))

        return value

    def clean_schedule_dow(self):

        value = self.cleaned_data['schedule_dow'].strip()
        if value == '*':
            return value
        try:
            n = int(value)
            if n < 0 or n > 6:
                raise Exception("invalid day of week specified (%s)" % value)
        except Exception as e:
            raise forms.ValidationError("Day of week must be either * or within interval [0:6]. Error: %s" % str(e))

        return value
