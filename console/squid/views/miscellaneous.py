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
from squid.models import Miscellaneous


#
#
#
class ViewMiscellaneous(SuccessMessageMixin, generic.edit.UpdateView):

    model           = Miscellaneous
    fields          = ['forwarded_for']
    template_name   = 'squid/settings/miscellaneous.html'
    success_message = 'need_squid_restart'

    def get_object(self):
        return Miscellaneous.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewMiscellaneous')

