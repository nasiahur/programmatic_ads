#
#
#
from django import forms
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy

#
#
#
from squid.models import Network

#
# network
#
class ViewNetworkInfo(SuccessMessageMixin, generic.edit.UpdateView):

    model           = Network
    fields          = '__all__'
    template_name   = 'squid/settings/network.html'
    success_message = 'need_squid_restart'

    def get_object(self):
        return Network.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewNetworkInfo')

    def form_valid(self, form):

        try:
            intercept_mode = form.cleaned_data['intercept_mode']
            if int(intercept_mode) == Network.INTERCEPT_MODE_WCCP:
                wccp2_router = form.cleaned_data['wccp2_router']
                if len(wccp2_router) == 0:
                    raise Exception("Please provide Cisco ASA firewall / Cisco router IP address. You need to configure it before enabling WCCPv2 interception.")

            return super(ViewNetworkInfo, self).form_valid(form)
            
        except Exception as e:        
            form.errors['__all__'] = form.error_class(["%s" % str(e)])

            # failure
            return super(ViewNetworkInfo, self).form_invalid(form)