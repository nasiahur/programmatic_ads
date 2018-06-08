#
#
#
from django import forms

#
#
#
from safety.models import ExclusionRange
from utility.validator import AddressRange

#
#
#
from exclusion_base import *

#
#
#
class ViewExclusionRangeList(ViewExclusionList):

    model         = ExclusionRange
    template_name = "safety/exclusions/range_list.html"


#
#
#
class ExclusionRangeForm(ExclusionForm):

    class Meta:
        model = ExclusionRange      
        fields = '__all__'  

    def clean_value(self):  
        return AddressRange().check(self.cleaned_data['value'])      


#
#
#
class ViewExclusionRangeCreate(ViewExclusionCreate):

    model           = ExclusionRange
    form_class      = ExclusionRangeForm
    template_name   = "safety/exclusions/range_form.html"


#
#
#
class ViewExclusionRangeUpdate(ViewExclusionUpdate):

    model           = ExclusionRange
    form_class      = ExclusionRangeForm
    template_name   = "safety/exclusions/range_form.html"
