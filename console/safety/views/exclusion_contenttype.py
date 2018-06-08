#
#
#
from django import forms

#
#
#
from safety.models import ExclusionContentType

#
#
#
from exclusion_base import *

#
#
#
class ViewExclusionContentTypeList(ViewExclusionList):

    model         = ExclusionContentType
    template_name = "safety/exclusions/contenttype_list.html"

    
#
#
#
class ExclusionContentTypeForm(ExclusionForm):

    class Meta:
        model = ExclusionContentType
        fields = '__all__'
        
    def clean_value(self):
        value = self.cleaned_data['value']        
        try:
            (part1, part2) = value.split("/")            
        except:
            raise forms.ValidationError("Specified Content Type value should be written as string/string, for example image/gif.")            
        return value.lower()


#
#
#
class ViewExclusionContentTypeCreate(ViewExclusionCreate):

    model           = ExclusionContentType
    form_class      = ExclusionContentTypeForm
    template_name   = "safety/exclusions/contenttype_form.html"

#
#
#
class ViewExclusionContentTypeUpdate(ViewExclusionUpdate):

    model           = ExclusionContentType
    form_class      = ExclusionContentTypeForm
    template_name   = "safety/exclusions/contenttype_form.html"
