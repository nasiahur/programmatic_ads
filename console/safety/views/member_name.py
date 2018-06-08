#
#
#
from safety.models import MemberName

#
#
#
from member_base import *

#
#
#
class ViewMemberNameList(ViewMemberList):

    model           = MemberName
    template_name   = "safety/members/name_list.html"

#
#
#
class MemberNameForm(MemberForm):

    class Meta:
        model = MemberName    
        fields = '__all__'

    def clean_value(self):
        return self.cleaned_data['value']


#
#
#
class ViewMemberNameCreate(ViewMemberCreate):

    model           = MemberName
    form_class      = MemberNameForm
    template_name   = "safety/members/name_form.html"

#
#
#
class ViewMemberNameUpdate(ViewMemberUpdate):

    model           = MemberName
    form_class      = MemberNameForm
    template_name   = "safety/members/name_form.html"
