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
from squid.models import Dns

#
#
#
class ViewDns(SuccessMessageMixin, generic.edit.UpdateView):

    model           = Dns
    fields          = ['dns_timeout', 'dns_nameservers', 'dns_v4_first']
    template_name   = 'squid/settings/dns.html'
    success_message = 'need_squid_restart'

    def get_object(self):
        return Dns.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewDns')