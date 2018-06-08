#
#
#
from django import forms
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import ByPassToken, Policy

#
#
#
from items import ViewItemList


#
#
#
class ViewSettingsByPass(SuccessMessageMixin, ViewItemList):
    
    model           = ByPassToken
    success_message = "need_squid_restart"
    template_name   = "safety/settings/bypasstoken_list.html"

    def get_success_url(self):
        return reverse("ViewSettingsByPass")

#
#
#    
class ViewSettingsByPassCreate(SuccessMessageMixin, generic.edit.CreateView): 
   
    model  = ByPassToken
    fields = ['name', 'value', 'comment']
    success_message = "need_squid_restart"
    template_name   = "safety/settings/bypasstoken_form.html"

    def get_success_url(self):
        return reverse("ViewSettingsByPass")

#
#
#
class ViewSettingsByPassUpdate(SuccessMessageMixin, generic.edit.UpdateView):

    model           = ByPassToken
    fields          = ['name', 'value', 'comment']
    success_message = "need_squid_restart"
    template_name   = "safety/settings/bypasstoken_form.html"

    def get_success_url(self):
        return reverse("ViewSettingsByPass")


#
#
#
class ByPassForm(forms.ModelForm):
    
    class Meta:

        model  = Policy
        fields = [
            'bypass_allowed', 
            'bypass_strip_www',
            'bypass_children',
            #'bypass_category',
            #'bypass_all',
            'bypass_referers',
            'bypass_duration', 
            'bypass_token_required', 
            'bypass_adult', 
            'bypass_categories', 
            'bypass_file', 
            'bypass_adblock',
            'bypass_privacy',
            'bypass_http'
        ]
    
#
#
#
class ViewByPass(SuccessMessageMixin, generic.edit.UpdateView):

    model           = Policy
    form_class      = ByPassForm
    template_name   = "safety/bypass_form.html"
    success_message = "need_squid_reload"

    def get_success_url(self):
        return reverse('ViewByPass', kwargs={'pk': self.kwargs['pk']})