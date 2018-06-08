#
#
#
from django import forms

#
#
#
from safety.models import ExclusionIp
from utility.validator import AddressIP

#
#
#
from exclusion_base import *

#
#
#
class ViewExclusionIpList(ViewExclusionList):

    model           = ExclusionIp
    template_name   = "safety/exclusions/ip_list.html"

#
#
#
class ExclusionIpForm(ExclusionForm):

    class Meta:
        model = ExclusionIp
        fields = '__all__'
        
    def clean_value(self):      
        return AddressIP().check(self.cleaned_data['value'])

#
#
#
class ViewExclusionIpCreate(ViewExclusionCreate):

    model           = ExclusionIp
    form_class      = ExclusionIpForm
    template_name   = "safety/exclusions/ip_form.html"

#
#
#
class ViewExclusionIpUpdate(ViewExclusionUpdate):

    model           = ExclusionIp
    form_class      = ExclusionIpForm
    template_name   = "safety/exclusions/ip_form.html"
