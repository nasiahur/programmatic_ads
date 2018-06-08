#
#
#
from django import forms
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect

#
#
#
from .items import \
    ViewItemList, \
    ViewItemCreate, \
    ViewItemUpdate, \
    ViewDomainNameCreate

from .forms import \
    ItemForm, \
    DomainNameForm, \
    IpForm, \
    SubnetForm, \
    RangeForm, \
    AdvancedForm

from squid.models import \
    ExcludeDomainName, ExcludeDomainIp, ExcludeDomainSubnet, ExcludeDomainRange, \
    ExcludeUserName, ExcludeUserIp, ExcludeUserSubnet, ExcludeUserRange, ExcludeUserAgent, \
    ExcludeContentType, \
    ExcludeSchedule, \
    ExcludeAdvanced, \
    ExcludeCategories

#
# exclude by domain name
#
class ViewExcludeDomainNameList(ViewItemList):

    model         = ExcludeDomainName
    template_name = "squid/exclude/domainname/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainNameList")

class ExcludeDomainNameForm(DomainNameForm):

    class Meta:
        model  = ExcludeDomainName
        fields = '__all__'

class ViewExcludeDomainNameCreate(ViewDomainNameCreate):

    model         = ExcludeDomainName
    form_class    = ExcludeDomainNameForm
    template_name = "squid/exclude/domainname/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainNameList")

class ViewExcludeDomainNameUpdate(ViewItemUpdate):

    model         = ExcludeDomainName
    form_class    = ExcludeDomainNameForm
    template_name = "squid/exclude/domainname/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainNameList")

#
# exclude by domain ip
#
class ViewExcludeDomainIpList(ViewItemList):

    model         = ExcludeDomainIp
    template_name = "squid/exclude/domainip/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainIpList")

class ExcludeDomainIpForm(IpForm):

    class Meta:
        model  = ExcludeDomainIp
        fields = '__all__'

class ViewExcludeDomainIpCreate(ViewItemCreate):

    model         = ExcludeDomainIp
    form_class    = ExcludeDomainIpForm
    template_name = "squid/exclude/domainip/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainIpList")

class ViewExcludeDomainIpUpdate(ViewItemUpdate):

    model         = ExcludeDomainIp
    form_class    = ExcludeDomainIpForm
    template_name = "squid/exclude/domainip/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainIpList")

#
# exclude by domain range
#
class ViewExcludeDomainRangeList(ViewItemList):

    model         = ExcludeDomainRange
    template_name = "squid/exclude/domainrange/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainRangeList")

class ExcludeDomainRangeForm(RangeForm):

    class Meta:
        model  = ExcludeDomainRange
        fields = '__all__'

class ViewExcludeDomainRangeCreate(ViewItemCreate):

    model         = ExcludeDomainRange
    form_class    = ExcludeDomainRangeForm
    template_name = "squid/exclude/domainrange/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainRangeList")

class ViewExcludeDomainRangeUpdate(ViewItemUpdate):

    model         = ExcludeDomainRange
    form_class    = ExcludeDomainRangeForm
    template_name = "squid/exclude/domainrange/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainRangeList")

#
# exclude by domain subnet
#
class ViewExcludeDomainSubnetList(ViewItemList):

    model         = ExcludeDomainSubnet
    template_name = "squid/exclude/domainsubnet/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainSubnetList")

class ExcludeDomainSubnetForm(SubnetForm):

    class Meta:
        model  = ExcludeDomainSubnet
        fields = '__all__'

class ViewExcludeDomainSubnetCreate(ViewItemCreate):

    model         = ExcludeDomainSubnet
    form_class    = ExcludeDomainSubnetForm
    template_name = "squid/exclude/domainsubnet/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainSubnetList")

class ViewExcludeDomainSubnetUpdate(ViewItemUpdate):

    model         = ExcludeDomainSubnet
    form_class    = ExcludeDomainSubnetForm
    template_name = "squid/exclude/domainsubnet/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeDomainSubnetList")

#
# exclude by user ip
#
class ViewExcludeUserIpList(ViewItemList):

    model         = ExcludeUserIp
    template_name = "squid/exclude/userip/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserIpList")

class ExcludeUserIpForm(IpForm):

    class Meta:
        model  = ExcludeUserIp
        fields = '__all__'

class ViewExcludeUserIpCreate(ViewItemCreate):

    model         = ExcludeUserIp
    form_class    = ExcludeUserIpForm
    template_name = "squid/exclude/userip/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserIpList")

class ViewExcludeUserIpUpdate(ViewItemUpdate):

    model         = ExcludeUserIp
    form_class    = ExcludeUserIpForm
    template_name = "squid/exclude/userip/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserIpList")

#
# exclude by user range
#
class ViewExcludeUserRangeList(ViewItemList):

    model         = ExcludeUserRange
    template_name = "squid/exclude/userrange/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserRangeList")

class ExcludeUserRangeForm(RangeForm):

    class Meta:
        model  = ExcludeUserRange
        fields = '__all__'

class ViewExcludeUserRangeCreate(ViewItemCreate):

    model         = ExcludeUserRange
    form_class    = ExcludeUserRangeForm
    template_name = "squid/exclude/userrange/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserRangeList")

class ViewExcludeUserRangeUpdate(ViewItemUpdate):

    model         = ExcludeUserRange
    form_class    = ExcludeUserRangeForm
    template_name = "squid/exclude/userrange/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserRangeList")

#
# exclude by user subnet
#
class ViewExcludeUserSubnetList(ViewItemList):

    model         = ExcludeUserSubnet
    template_name = "squid/exclude/usersubnet/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserSubnetList")

class ExcludeUserSubnetForm(SubnetForm):

    class Meta:
        model  = ExcludeUserSubnet
        fields = '__all__'

class ViewExcludeUserSubnetCreate(ViewItemCreate):

    model         = ExcludeUserSubnet
    form_class    = ExcludeUserSubnetForm
    template_name = "squid/exclude/usersubnet/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserSubnetList")

class ViewExcludeUserSubnetUpdate(ViewItemUpdate):

    model         = ExcludeUserSubnet
    form_class    = ExcludeUserSubnetForm
    template_name = "squid/exclude/usersubnet/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserSubnetList")

#
# exclude by user agent
#
class ViewExcludeUserAgentList(ViewItemList):

    model         = ExcludeUserAgent
    template_name = "squid/exclude/useragent/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserAgentList")

class ExcludeUserAgentForm(ItemForm):

    class Meta:
        model  = ExcludeUserAgent
        fields = '__all__'

class ViewExcludeUserAgentCreate(ViewItemCreate):

    model         = ExcludeUserAgent
    form_class    = ExcludeUserAgentForm
    template_name = "squid/exclude/useragent/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserAgentList")

class ViewExcludeUserAgentUpdate(ViewItemUpdate):

    model         = ExcludeUserAgent
    form_class    = ExcludeUserAgentForm
    template_name = "squid/exclude/useragent/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeUserAgentList")

#
# exclude by content type
#
class ViewExcludeContentTypeList(ViewItemList):

    model         = ExcludeContentType
    template_name = "squid/exclude/contenttype/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeContentTypeList")

class ExcludeContentTypeForm(ItemForm):

    class Meta:
        model  = ExcludeContentType
        fields = '__all__'

    def clean_value(self):
        value = self.cleaned_data['value']        
        try:
            (part1, part2) = value.split("/")            
        except:
            raise forms.ValidationError("Specified Content Type value should be written as string/string, for example image/gif.")            
        return value.lower()

class ViewExcludeContentTypeCreate(ViewItemCreate):

    model         = ExcludeContentType
    form_class    = ExcludeContentTypeForm
    template_name = "squid/exclude/contenttype/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeContentTypeList")

class ViewExcludeContentTypeUpdate(ViewItemUpdate):

    model         = ExcludeContentType
    form_class    = ExcludeContentTypeForm
    template_name = "squid/exclude/contenttype/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeContentTypeList")

#
# exclude by schedule
#
class ViewExcludeScheduleList(ViewItemList):

    model         = ExcludeSchedule
    template_name = "squid/exclude/schedule/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeScheduleList")

class ExcludeScheduleForm(ItemForm):

    class Meta:
        model  = ExcludeSchedule
        fields = '__all__'

class ViewExcludeScheduleCreate(ViewItemCreate):

    model         = ExcludeSchedule
    form_class    = ExcludeScheduleForm
    template_name = "squid/exclude/schedule/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeScheduleList")

class ViewExcludeScheduleUpdate(ViewItemUpdate):

    model         = ExcludeSchedule
    form_class    = ExcludeScheduleForm
    template_name = "squid/exclude/schedule/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeScheduleList")

#
# exclude advanced
#

class ViewExcludeBase(ViewItemUpdate):

    model = ExcludeAdvanced
    
    def get_object(self): 
        return ExcludeAdvanced.objects.first()

class ViewExcludeAdvancedSsl(ViewExcludeBase):

    fields        = ['value_sslbump']
    template_name = "squid/exclude/advanced/form_ssl.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeAdvancedSsl")


class ViewExcludeAdvancedAdaptation(ViewExcludeBase):

    fields        = ['value_adaptation']
    template_name = "squid/exclude/advanced/form_adaptation.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeAdvancedAdaptation")


class ViewExcludeAdvancedAuth(ViewExcludeBase):

    fields        = ['value_auth']
    template_name = "squid/exclude/advanced/form_auth.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeAdvancedAuth")

class ViewExcludeAdvancedCache(ViewExcludeBase):

    fields        = ['value_cache']
    template_name = "squid/exclude/advanced/form_cache.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeAdvancedCache")

class ViewExcludeAdvancedUrlRewriter(ViewExcludeBase):

    fields        = ['value_urlrewrite']
    template_name = "squid/exclude/advanced/form_urlrewriter.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeAdvancedUrlRewriter")


#
# exclude by category
#
class ExcludeCategoriesForm(AdvancedForm):

    class Meta:
        model  = ExcludeCategories
        fields = '__all__'

class ViewExcludeCategoryUpdate(ViewItemUpdate):

    model           = ExcludeCategories
    form_class      = ExcludeCategoriesForm
    success_message = "need_squid_restart"
    template_name   = "squid/exclude/categories/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewExcludeCategoryUpdate")

    def get_object(self): 
        return ExcludeCategories.objects.first()