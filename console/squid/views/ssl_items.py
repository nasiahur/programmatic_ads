import os
import traceback

#
# domain logic (non django)
#
from _domain.core import Paths
from _domain.squid import CertificateParser, CertificateFactory

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
from django.http import HttpResponse, HttpResponseRedirect

#
#
#
from utility.views import ListViewTransposer

from .items import \
    ViewItemList, \
    ViewItemCreate, \
    ViewItemUpdate, \
    ViewDomainNameCreate

from .forms import \
    DomainNameForm, \
    IpForm, \
    SubnetForm, \
    AdvancedForm

from squid.models import \
    SslTargetDomain, \
    SslTargetIp, \
    SslTargetSubnet, \
    SslErrorDomain, \
    SslErrorIp, \
    SslErrorSubnet, \
    SslIntermediateCert

#
# ssl target domain name
#
class ViewSslTargetDomainList(ViewItemList):

    model         = SslTargetDomain
    template_name = "squid/ssl/target/domainname/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetDomainList")

class SslTargetDomainForm(DomainNameForm):

    class Meta:
        model  = SslTargetDomain
        fields = '__all__'

class ViewSslTargetDomainCreate(ViewDomainNameCreate):

    model         = SslTargetDomain
    form_class    = SslTargetDomainForm
    template_name = "squid/ssl/target/domainname/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetDomainList")

class ViewSslTargetDomainUpdate(ViewItemUpdate):

    model         = SslTargetDomain
    form_class    = SslTargetDomainForm
    template_name = "squid/ssl/target/domainname/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetDomainList")

#
# ssl target ip 
#
class ViewSslTargetIpList(ViewItemList):

    model         = SslTargetIp
    template_name = "squid/ssl/target/domainip/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetIpList")

class SslTargetIpForm(IpForm):

    class Meta:
        model  = SslTargetIp
        fields = '__all__'

class ViewSslTargetIpCreate(ViewItemCreate):

    model         = SslTargetIp
    form_class    = SslTargetIpForm
    template_name = "squid/ssl/target/domainip/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetIpList")

class ViewSslTargetIpUpdate(ViewItemUpdate):

    model         = SslTargetIp
    form_class    = SslTargetIpForm
    template_name = "squid/ssl/target/domainip/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetIpList")

#
# ssl target subnet
#
class ViewSslTargetSubnetList(ViewItemList):

    model         = SslTargetSubnet
    template_name = "squid/ssl/target/domainsubnet/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetSubnetList")

class SslTargetSubnetForm(SubnetForm):

    class Meta:
        model  = SslTargetSubnet
        fields = '__all__'

class ViewSslTargetSubnetCreate(ViewItemCreate):

    model         = SslTargetSubnet
    form_class    = SslTargetSubnetForm
    template_name = "squid/ssl/target/domainsubnet/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetSubnetList")

class ViewSslTargetSubnetUpdate(ViewItemUpdate):

    model         = SslTargetSubnet
    form_class    = SslTargetSubnetForm
    template_name = "squid/ssl/target/domainsubnet/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslTargetSubnetList")

#
# ssl error domain name
#
class ViewSslErrorDomainList(ViewItemList):

    model         = SslErrorDomain
    template_name = "squid/ssl/errors/domainname/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorDomainList")

class SslErrorDomainForm(DomainNameForm):

    class Meta:
        model  = SslErrorDomain
        fields = '__all__'

class ViewSslErrorDomainCreate(ViewDomainNameCreate):

    model         = SslErrorDomain
    form_class    = SslErrorDomainForm
    template_name = "squid/ssl/errors/domainname/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorDomainList")

class ViewSslErrorDomainUpdate(ViewItemUpdate):

    model         = SslErrorDomain
    form_class    = SslErrorDomainForm
    template_name = "squid/ssl/errors/domainname/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorDomainList")

#
# ssl error ip 
#
class ViewSslErrorIpList(ViewItemList):

    model         = SslErrorIp
    template_name = "squid/ssl/errors/domainip/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorIpList")

class SslErrorIpForm(IpForm):

    class Meta:
        model  = SslErrorIp
        fields = '__all__'

class ViewSslErrorIpCreate(ViewItemCreate):

    model         = SslErrorIp
    form_class    = SslErrorIpForm
    template_name = "squid/ssl/errors/domainip/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorIpList")

class ViewSslErrorIpUpdate(ViewItemUpdate):

    model         = SslErrorIp
    form_class    = SslErrorIpForm
    template_name = "squid/ssl/errors/domainip/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorIpList")

#
# ssl error subnet
#
class ViewSslErrorSubnetList(ViewItemList):

    model         = SslErrorSubnet
    template_name = "squid/ssl/errors/domainsubnet/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorSubnetList")

class SslErrorSubnetForm(SubnetForm):

    class Meta:
        model  = SslErrorSubnet
        fields = '__all__'

class ViewSslErrorSubnetCreate(ViewItemCreate):

    model         = SslErrorSubnet
    form_class    = SslErrorSubnetForm
    template_name = "squid/ssl/errors/domainsubnet/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorSubnetList")

class ViewSslErrorSubnetUpdate(ViewItemUpdate):

    model         = SslErrorSubnet
    form_class    = SslErrorSubnetForm
    template_name = "squid/ssl/errors/domainsubnet/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslErrorSubnetList")


#
# missing intermediate certificate list
#
class ViewSslIntermediateCertList(ViewItemList):

    model         = SslIntermediateCert
    template_name = "squid/ssl/missing/list.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslIntermediateCertList")

class SslIntermediateCertUploadForm(forms.ModelForm):

    class Meta:
        model  = SslIntermediateCert
        fields = []

    file = forms.FileField()

class ViewSslIntermediateCertCreate(ViewItemCreate):

    model         = SslIntermediateCert
    form_class    = SslIntermediateCertUploadForm
    template_name = "squid/ssl/missing/form.html"
    
    def get_success_url(self): 
        return reverse_lazy("ViewSslIntermediateCertList")

    def form_valid(self, form):

        try:
            # parse the uploaded PEM into the list of certificates
            payload = self.get_payload(self.request)
            pems    = self.get_pems(payload)

            # perfect now construct certificate object out of these pems
            certs = self.get_certs(pems)

            # loop through each cert and add it
            for cert in certs:

                # is subject key identifier present?
                if 'subjectKeyIdentifier' not in cert.extensions:
                    continue

                identifier = cert.extensions['subjectKeyIdentifier']
                if not identifier:
                    continue

                # ok we have the identifier, try to look it up in the list or create
                item = None                

                existing_set = SslIntermediateCert.objects.filter(subject_keyid=identifier)
                if len(existing_set) > 0:
                    item = existing_set[0]
                else:
                    item = SslIntermediateCert(subject_keyid=identifier)

                # save fields (eventually overwriting all of the existing object)
                item.pem = cert.pem
                item.serial_num  = cert.hex_sn()
                item.subject     = cert.subject
                item.common_name = cert.common_name()
                #alt_names     = models.CharField(max_length=254)
                item.valid_from  = cert.valid_from()
                item.valid_until = cert.valid_until()
                #issuer        = models.CharField(max_length=254)

                item.save()

            messages.info(self.request, self.success_message)
            
            # ok if we got here everything is fine
            return HttpResponseRedirect(reverse_lazy("ViewSslIntermediateCertList"))
            
        except Exception as e:        

            # add errors to collection of form errors
            form.errors['__all__']   = form.error_class(["%s" % str(e)])
            form.errors['traceback'] = str(traceback.format_exc())

            # failure
            return super(ViewSslIntermediateCertCreate, self).form_invalid(form)

    def get_payload(self, request):

        data    = request.FILES['file']
        payload = ""
        for chunk in data.chunks():
            payload += chunk
        return payload

    def get_pems(self, pem_str):

        parser = CertificateParser()
        result = parser.parse(pem_str)

        return result

    def get_certs(self, pems):

        factory = CertificateFactory()
        result  = factory.construct(pems)

        return result

class ViewSslIntermediateCertBackUp(generic.View):

    def get(self, request, *args, **kwargs):            

        # construct the path
        path = os.path.join(Paths.etc_dir(), "squid", "foreign_intermediate_certs.pem")

        # if no file exist, create it
        if not os.path.isfile(path):
            with open(path, "wb") as fin:
                pass

        # and send contents
        with open(path, "rb") as fin:
            response = HttpResponse(fin.read(), content_type="application/x-x509-ca-cert")
            response['Content-Disposition'] = "attachment; filename=\"%s\"" % "foreign_intermediate_certs.pem"
            return response
