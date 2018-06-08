import pytz
import traceback

#
#
#
from django import forms
from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from _domain.node import TimeZone

#
#
#
class TimeZoneForm(forms.Form):
    value = forms.ChoiceField(choices=[ (tz, str(tz)) for tz in list(pytz.all_timezones) ])

#
#
#
class TimeZoneReboot:

    required      = False
    error         = False
    error_msg     = ""
    configured_tz = ""
    running_tz    = ""
    
    def __init__(self):

        try:
            self.configured_tz = TimeZone().configured_tz()
            self.running_tz    = TimeZone().running_tz()

            if self.configured_tz != self.running_tz:
                self.required = True

        except Exception as e:
            self.error     = True
            self.error_msg = "%s:%s" % (str(e), traceback.format_exc())

#
#
#
class ViewTimeZone(SuccessMessageMixin, generic.View):

    template_name = "node/timezone/timezone_form.html"
    form_class    = TimeZoneForm

    def get_success_url(self):
        return reverse_lazy('node:ViewTimeZone')

    def get(self, request, *args, **kwargs):
        data = {
            'value'  : TimeZone().configured_tz()
        }
        context = {
            'form'   : TimeZoneForm(initial=data), 
            'reboot' : TimeZoneReboot()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = TimeZoneForm(request.POST)
        if form.is_valid():

            try:
                timezone = form.cleaned_data.get('value', '')            
                if len(timezone) == 0:
                    raise Exception("Empty time zone is not allowed.")

                # write to the system
                (ret, stdout, stderr) = TimeZone().set(timezone)
                if ret != 0:
                    raise Exception("Cannot set timezone to '%s'. Error: %d (stdout: %s, stderr: %s)" % (timezone, ret, stdout, stderr))

                # tell the user
                messages.info(self.request, "need_reboot")

                return HttpResponseRedirect(self.get_success_url())
                
            except Exception as e:        
                form.errors['__all__']   = form.error_class(["%s\n%s" % (str(e), traceback.format_exc())])
                
        # if we got here, POST failed
        context = {
            'form'   : form, 
            'reboot' : TimeZoneReboot()
        }
        return render(request, self.template_name, context )