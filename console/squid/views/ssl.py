import os
import traceback

#
# domain logic (non django)
#
from _domain.core import Paths
from _domain.squid import SquidCert


#
#
#
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from squid.models import BumpMode

#
#
#
class ViewSslInfo(generic.base.TemplateView):

    template_name='squid/ssl/mode.html'

    def get_context_data(self, **kwargs):
        
        context = super(ViewSslInfo, self).get_context_data(**kwargs)    

        result = False 
        cert   = None
        error  = ""

        try:
            cert   = SquidCert().get()
            result = True

        except Exception as e:
            result = False
            error  = "%s\nStack:%s" % (str(e), traceback.format_exc())

        context['cert']     = cert
        context['result']   = result
        context['error']    = error
        context['bumpmode'] = BumpMode.objects.first()
        

        return context

#
#
#
class ViewSslMode(generic.View):

    success_message = "need_squid_restart"
    
    def post(self, request, *args, **kwargs):

        bumpmode = BumpMode.objects.first()
        value    = request.POST.get('bump_all', '0')
        if value == '1':
            bumpmode.value = BumpMode.BUMPMODE_BUMPALL
        else:
            bumpmode.value = BumpMode.BUMPMODE_SELECTED
        
        bumpmode.save()
        
        messages.info(self.request, self.success_message)   

        return HttpResponseRedirect(reverse_lazy("ViewSslInfo"))

#
#
#
class ViewSslDer(generic.View):

    def get(self, request, *args, **kwargs):  

        path = os.path.join(Paths.etc_dir(), "myca.der")
        with open(path, "rb") as fin:
            response = HttpResponse(fin.read(), content_type="application/x-x509-ca-cert")
            response['Content-Disposition'] = "attachment; filename=\"%s\"" % "myca.der"
            return response

#
#
#
class ViewSslPemBackUp(generic.View):

    def get(self, request, *args, **kwargs):            

        path = os.path.join(Paths.etc_dir(), "myca.pem")
        with open(path, "rb") as fin:
            response = HttpResponse(fin.read(), content_type="application/x-x509-ca-cert")
            response['Content-Disposition'] = "attachment; filename=\"%s\"" % "myca.pem"
            return response

#
#
#
class PemUploadForm(forms.Form):
    file = forms.FileField()

#
#
#
class ViewSslPemUpload(SuccessMessageMixin, generic.edit.FormView):

    form_class      = PemUploadForm
    template_name   = 'squid/ssl/pem_upload.html'
    success_message = 'need_squid_restart'
    
    def get_success_url(self): 
        return reverse_lazy('ViewSslInfo')

    def form_valid(self, form):

        try:
            # get data
            data = self.request.FILES['file']

            # upload it
            cert = SquidCert()
            cert.upload(data)
            
            # ok if we got here everything is fine
            return super(ViewSslPemUpload, self).form_valid(form)
            
        except Exception as e:        

            # convert error to string
            error = "%s%s" % (str(e), traceback.format_exc())

            # and add it to collection of form errors
            form.errors['__all__'] = form.error_class([error])

            # failure
            return super(ViewSslPemUpload, self).form_invalid(form)
#
#
#
class PemGenerateForm(forms.Form):

    newCertSupportEMail = forms.CharField(max_length=64)
    newCertCommonName   = forms.CharField(max_length=64)
    newCertLifeTime     = forms.IntegerField(widget=forms.TextInput())
    newCertOrganization = forms.CharField(max_length=64)
    newCertOU           = forms.CharField(max_length=64)
    newCertCountry      = forms.CharField(max_length=2)
    newCertState        = forms.CharField(max_length=64)
    newCertCity         = forms.CharField(max_length=64)


class ViewSslPemGenerate(SuccessMessageMixin, generic.edit.FormView):

    form_class      = PemGenerateForm
    template_name   = 'squid/ssl/pem_generate.html'
    success_message = 'need_squid_restart'
    
    def get_success_url(self): 
        return reverse_lazy('ViewSslInfo')

    def form_valid(self, form):

        try:

            # generate it
            cert = SquidCert()
            cert.generate(
                form.cleaned_data['newCertCountry'],
                form.cleaned_data['newCertState'],
                form.cleaned_data['newCertCity'],
                form.cleaned_data['newCertOrganization'],
                form.cleaned_data['newCertOU'],
                form.cleaned_data['newCertSupportEMail'],
                form.cleaned_data['newCertCommonName'],
                form.cleaned_data['newCertLifeTime']
            )

            # ok if we got here everything is fine
            return super(ViewSslPemGenerate, self).form_valid(form)

        except Exception as e:        

            # convert error to string
            error = "%s%s" % (str(e), traceback.format_exc())

            # and add it to collection of form errors
            form.errors['__all__'] = form.error_class([error])

            # failure
            return super(ViewSslPemGenerate, self).form_invalid(form)