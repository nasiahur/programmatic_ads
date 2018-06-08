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
from squid.models import AclDefault
    

#
# acls
#
class ViewAcls(SuccessMessageMixin, generic.edit.UpdateView):

    model           = AclDefault
    fields          = '__all__'
    template_name   = 'squid/settings/acls.html'
    success_message = 'need_squid_restart'

    def get_object(self):
        return AclDefault.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewAcls')