#
#
#
from safety.models import MemberRange
from utility.validator import AddressRange

#
#
#
from member_base import *

#
#
#
class ViewMemberRangeList(ViewMemberList):

    model         = MemberRange
    template_name = "safety/members/range_list.html"

#
#
#
class MemberRangeForm(MemberForm):

    class Meta:
        model = MemberRange    
        fields = '__all__'

    def clean_value(self):
        return AddressRange().check(self.cleaned_data['value'])

#
#
#
class ViewMemberRangeCreate(ViewMemberCreate):

    model           = MemberRange
    form_class      = MemberRangeForm
    template_name   = "safety/members/range_form.html"

#
#
#
class ViewMemberRangeUpdate(ViewMemberUpdate):

    model           = MemberRange
    form_class      = MemberRangeForm
    template_name   = "safety/members/range_form.html"
