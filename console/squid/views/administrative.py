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
from squid.models import Administrative
    
#
#
#
class ViewAdministrative(SuccessMessageMixin, generic.edit.UpdateView):

    model           = Administrative
    fields          = ['cache_mgr', 'httpd_suppress_version_string', 'visible_hostname']
    template_name   = 'squid/settings/administrative.html'
    success_message = 'need_squid_restart'

    def get_object(self):
        return Administrative.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewAdministrative')

    '''
    def get_context_data(self, **kwargs):

        context = super(ViewAdministrative, self).get_context_data(**kwargs)        
        squid   = self.request.user.profile.squid

        context['squid'] = squid
        return context
    '''