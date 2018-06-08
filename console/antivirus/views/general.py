#
#
#
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from antivirus.models import AvSettings


#
#
#
class ViewAvSettingsMode(SuccessMessageMixin, generic.edit.UpdateView):

    model           = AvSettings
    fields          = ['enable', 'av_type', 'bypass_to_localnet']
    success_message = "need_squid_restart"
    template_name   = "antivirus/settings/mode_form.html"

    def get_object(self):
        return AvSettings.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewAvSettingsMode")

#
#
#
class ViewAvSettingsEcapActions(SuccessMessageMixin, generic.edit.UpdateView):

    model  = AvSettings
    fields = [ 
        'ecap_clamav_async', 
        'ecap_clamav_message_size_max', 
        'ecap_clamav_on_error_action',
        'ecap_reqmod_bypass',
        'ecap_respmod_bypass'
    ]
    success_message = "need_squid_restart"
    template_name   = "antivirus/settings/ecap_actions_form.html"

    def get_object(self):
        return AvSettings.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewAvSettingsEcapActions")

#
#
#
class ViewAvSettingsEcapTrickling(SuccessMessageMixin, generic.edit.UpdateView):

    model  = AvSettings
    fields = [ 
        'ecap_clamav_trickling_enable', 
        'ecap_clamav_trickling_drop_size', 
        'ecap_clamav_trickling_period', 
        'ecap_clamav_trickling_type', 
        'ecap_clamav_trickling_size_max', 
        'ecap_clamav_trickling_start_delay', 
    ]
    success_message = "need_squid_restart"
    template_name   = "antivirus/settings/ecap_trickling_form.html"

    def get_object(self):
        return AvSettings.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewAvSettingsEcapTrickling")

#
#
#
class ViewAvSettingsIcap(SuccessMessageMixin, generic.edit.UpdateView):

    model  = AvSettings
    fields = [
        'avicap_address', 
        'avicap_port', 
        'avicap_reqpath', 
        'avicap_respath', 
        'avicap_res_bypass', 
        'avicap_options'
    ]
    success_message = "need_squid_restart"
    template_name   = "antivirus/settings/icap_form.html"

    def get_object(self):
        return AvSettings.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewAvSettingsIcap")
