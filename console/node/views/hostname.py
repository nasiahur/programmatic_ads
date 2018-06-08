import os
import traceback

#
#
#
from django import forms
from django.views import generic
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from _domain.node import HostName

#
#
#
class HostNameForm(forms.Form):

    value = forms.CharField(max_length=64)

#
#
#
class HostNameReboot:

    required      = False
    error         = False
    error_msg     = ""
    configured_hn = ""
    running_hn    = ""
    
    def __init__(self):

        try:
            self.configured_hn = HostName().configured_hostname()
            self.running_hn    = HostName().running_hostname()

            if self.configured_hn != self.running_hn:
                self.required = True

        except Exception as e:
            self.error     = True
            self.error_msg = "%s:%s" % (str(e), traceback.format_exc())

#
#
#    
class ViewHostName(SuccessMessageMixin, generic.View):

    template_name = "node/hostname/hostname_form.html"
    form_class    = HostNameForm

    def get_success_url(self):
        return reverse_lazy('node:ViewHostName')

    def get(self, request, *args, **kwargs):
        info = HostName()
        data = {
            'value'  : info.configured_hostname()
        }
        context = {
            'form'   : HostNameForm(initial=data), 
            'reboot' : HostNameReboot()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = HostNameForm(request.POST)
        if form.is_valid():

            try:
                hostname = form.cleaned_data.get('value', '')
                if len(hostname) == 0:
                    raise Exception("Empty host name is not allowed.")

                # write to the system
                (ret, stdout, stderr) = HostName().set(hostname)
                if ret != 0:
                    raise Exception("Cannot set host name to '%s'. Error: %d (stdout: %s, stderr: %s)" % (timezone, ret, stdout, stderr))

                # tell the user
                messages.info(self.request, "need_reboot")

                return HttpResponseRedirect(self.get_success_url())
                
            except Exception as e:        
                form.errors['__all__']   = form.error_class(["%s\n%s" % (str(e), traceback.format_exc())])
                
        # if we got here, POST failed
        context = {
            'form'   : form, 
            'reboot' : HostNameReboot()
        }
        return render(request, self.template_name, context)