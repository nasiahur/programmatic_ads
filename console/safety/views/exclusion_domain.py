#
#
#
from django import forms

#
#
#
from safety.models import ExclusionDomain

#
#
#
from exclusion_base import *

#
#
#
class ViewExclusionDomainList(ViewExclusionList):

    model         = ExclusionDomain
    template_name = "safety/exclusions/domain_list.html"

#
#
#
class ExclusionDomainForm(ExclusionForm):
    
    class Meta:
        model  = ExclusionDomain
        fields = '__all__'

    def clean_value(self):        
        value = self.cleaned_data['value']
        if "?" in value or "*" in value:
            raise forms.ValidationError("Domain '%s' cannot be added, becase it contains wildcards which are not supported." % value)
        return value.lower()

#
#
#
class ViewExclusionDomainCreate(ViewExclusionCreate):

    model           = ExclusionDomain
    form_class      = ExclusionDomainForm
    template_name   = "safety/exclusions/domain_form.html"

#
#
#
class ViewExclusionDomainUpdate(ViewExclusionUpdate):

    model           = ExclusionDomain
    form_class      = ExclusionDomainForm
    template_name   = "safety/exclusions/domain_form.html"
