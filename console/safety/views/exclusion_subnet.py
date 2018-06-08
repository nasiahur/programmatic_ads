#
#
#
from django import forms

#
#
#
from safety.models import ExclusionSubnet
from utility.validator import AddressSubnet

#
#
#
from exclusion_base import *

#
#
#
class ViewExclusionSubnetList(ViewExclusionList):

    model           = ExclusionSubnet
    template_name   = "safety/exclusions/subnet_list.html"

#
#
#
class ExclusionSubnetForm(ExclusionForm):

    class Meta:
        model = ExclusionSubnet
        fields = '__all__'
        
    def clean_value(self):      
        return AddressSubnet().check(self.cleaned_data['value'])


#
#
#
class ViewExclusionSubnetCreate(ViewExclusionCreate):

    model           = ExclusionSubnet
    form_class      = ExclusionSubnetForm
    template_name   = "safety/exclusions/subnet_form.html"

#
#
#
class ViewExclusionSubnetUpdate(ViewExclusionUpdate):

    model           = ExclusionSubnet
    form_class      = ExclusionSubnetForm
    template_name   = "safety/exclusions/subnet_form.html"
