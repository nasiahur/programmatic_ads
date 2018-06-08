#
#
#
from safety.models import MemberIp
from utility.validator import AddressIP

#
#
#
from member_base import *

#
#
#
class ViewMemberIpList(ViewMemberList):

    model         = MemberIp
    template_name = "safety/members/ip_list.html"

#
#
#
class MemberIpForm(MemberForm):

    class Meta:
        model = MemberIp    
        fields = '__all__'

    def clean_value(self):
        return AddressIP().check(self.cleaned_data['value'])

#
#
#
class ViewMemberIpCreate(ViewMemberCreate):

    model           = MemberIp
    form_class      = MemberIpForm
    template_name   = "safety/members/ip_form.html"

#
#
#
class ViewMemberIpUpdate(ViewMemberUpdate):

    model           = MemberIp
    form_class      = MemberIpForm
    template_name   = "safety/members/ip_form.html"
