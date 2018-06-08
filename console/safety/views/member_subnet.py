#
#
#
from safety.models import MemberSubnet
from utility.validator import AddressSubnet

#
#
#
from member_base import *

#
#
#
class ViewMemberSubnetList(ViewMemberList):

    model         = MemberSubnet
    template_name = "safety/members/subnet_list.html"

#
#
#
class MemberSubnetForm(MemberForm):

    class Meta:
        model = MemberSubnet    
        fields = '__all__'

    def clean_value(self):
        return AddressSubnet().check(self.cleaned_data['value'])

#
#
#
class ViewMemberSubnetCreate(ViewMemberCreate):

    model           = MemberSubnet
    form_class      = MemberSubnetForm
    template_name   = "safety/members/subnet_form.html"

#
#
#
class ViewMemberSubnetUpdate(ViewMemberUpdate):

    model           = MemberSubnet
    form_class      = MemberSubnetForm
    template_name   = "safety/members/subnet_form.html"
