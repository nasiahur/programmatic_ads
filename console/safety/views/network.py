import multiprocessing

#
#
#
from django import forms
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import Network
from utility.validator import AddressIP, PortIP


class NetworkForm(forms.ModelForm):

    class Meta:
        model  = Network
        fields = '__all__'
        
    def clean_wsicap_address(self): 
        return AddressIP().check(self.cleaned_data['wsicap_address'])

    def clean_wsicap_port(self):      
        return PortIP().check(self.cleaned_data['wsicap_port'])

    def clean_wsicap_threads(self):      
        value = self.cleaned_data['wsicap_threads']
        if value < 1 or value > 32:
            recommended = multiprocessing.cpu_count() * 2 + 1
            if recommended > 32:
                recommended = 32
            if recommended < 1:
                recommended = 3                
            raise forms.ValidationError("Number of threads must be within [1, 32], recommended for your system - %d." % recommended)
        return value


#
#
#
class ViewSettingsNetwork(SuccessMessageMixin, generic.edit.UpdateView):

    model      = Network
    form_class = NetworkForm
    success_message = "need_squid_restart"
    template_name   = "safety/settings/network_form.html"

    def get_object(self):
        return Network.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewSettingsNetwork")

