import re

#
#
#
from django import forms

#
#
#
from safety.models import ExclusionUrl
from utility.validator import AddressRange

#
#
#
from exclusion_base import *

#
#
#
class ViewExclusionUrlList(ViewExclusionList):

    model           = ExclusionUrl
    template_name   = "safety/exclusions/url_list.html"

#
#
#
class ExclusionUrlForm(ExclusionForm):

    class Meta:
        model = ExclusionUrl
        fields = '__all__'
        
    def clean_value(self):        
        value = self.cleaned_data['value']
        try:
            r = re.compile(value)
        except Exception as e:
            raise forms.ValidationError("Incorrect URL regex specified, regex compilation failed, error: %s" % str(e))
        return value


#
#
#
class ViewExclusionUrlCreate(ViewExclusionCreate):

    model           = ExclusionUrl
    form_class      = ExclusionUrlForm
    template_name   = "safety/exclusions/url_form.html"

#
#
#
class ViewExclusionUrlUpdate(ViewExclusionUpdate):

    model           = ExclusionUrl
    form_class      = ExclusionUrlForm
    template_name   = "safety/exclusions/url_form.html"
