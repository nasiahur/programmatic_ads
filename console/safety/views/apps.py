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
from safety.models import Apps

#
#
#
class AppsForm(forms.ModelForm):

    class Meta:
        model  = Apps
        fields = '__all__'
        
    google_apps_allowed_domains = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'size':'50','class':'input-block-level'}), required=False)
    
#
#
#
class ViewSettingsApps(SuccessMessageMixin, generic.edit.UpdateView):

    success_message = "need_squid_restart"
    model           = Apps
    form_class      = AppsForm
    template_name   = "safety/settings/apps_form.html"

    def get_object(self):
        return Apps.objects.first()

    def get_success_url(self):
        return reverse("ViewSettingsApps")