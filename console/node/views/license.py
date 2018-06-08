import os
import json
import shutil
import traceback

#
#
#
from _domain.core import Paths
from _domain.utils import LicenseManager, LicensedDevicesCounter, CommandLicense

#
#
#
from django import forms
from django.views import generic
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from safety.models import Network
from node.models import Sharing

#
#
#
class LicenseUploadForm(forms.Form):
    file = forms.FileField()

#
#
#
class ViewLicense(SuccessMessageMixin, generic.edit.FormView):

    template_name   = 'node/license.html'
    form_class      = LicenseUploadForm
    success_message = "need_squid_restart"

    def get_success_url(self):
        return reverse_lazy("node:ViewLicense")

    def get_context_data(self, **kwargs):
        
        context = super(ViewLicense, self).get_context_data(**kwargs)

        # see how many filtered devices are filtered
        context['filtered'] = int(LicensedDevicesCounter().get())
        
        # check the license
        (result, param2) = LicenseManager().get()
        if result is True:
            context['license']  = param2
            context['maxcount'] = int(param2['user_count'])
        else:
            context['error']    = param2
            context['maxcount'] = 0

        # and return
        return context

    def form_valid(self, form):

        try:
            # try to restore config
            self.install_license()

            # if we got here, restore was successful
            return super(ViewLicense, self).form_valid(form)

        except Exception as e:

            # in case of error, dump it
            form.errors['__all__']   = form.error_class(["%s" % str(e)])
            form.errors['traceback'] = "%s" % traceback.format_exc()

            # and fail
            return super(ViewLicense, self).form_invalid(form)

    def collect_license(self):

        # will write license data to a temp folder
        folder = os.path.join(Paths.var_dir(), "temp", "license_upload")
        try:
            shutil.rmtree(folder)
        except Exception as e:
            pass
        os.makedirs(folder)

        # collect all chunks into it        
        data = self.request.FILES['file']
        name = os.path.join(folder, "license.pem")

        try:
            os.unlink(name)
        except Exception as e:
            pass

        with open(name, "wb") as fout:
            for chunk in data.chunks():
                fout.write(chunk)

        # also copy out the diladele.pem and websafety.pem files into temp folder too
        shutil.copy(
            os.path.join(Paths.etc_dir(), "diladele.pem"),
            os.path.join(folder, "diladele.pem")
        )

        shutil.copy(
            os.path.join(Paths.etc_dir(), "websafety.pem"),
            os.path.join(folder, "websafety.pem")
        )

        # fine, license is there
        return folder

    def activate_safety(self):

        # get network object
        network = Network.objects.first()
        sharing = Sharing.objects.first()

        try:

            # check the license again
            (result, param2) = LicenseManager().get()

            # ok license check succeeded
            if result is True:

                # for convinience
                license = param2

                # see if it is valid
                if license["valid"] == "1":

                    # in community license we disable icap
                    if license['type'] == "community":
                        
                        network.enable_icap             = False
                        sharing.upload_recategorization = True
                        sharing.upload_telemetry_basic  = True

                    else:
                        network.enable_icap = True

                    # and save the new status
                    network.save()
                    sharing.save()

        except Exception as e:

            # never throws!
            pass

    def install_license(self):

        # collect the license into a temporary folder
        folder = self.collect_license()

        # protect against users loading key instead of pem
        if os.path.getsize(os.path.join(folder, "license.pem")) < 255:
            raise Exception("You might be uploading a 4.2 style license.key file. This version requires license.pem instead. Contact support@diladele.com to get it.")

        # check if the license is fine
        try:
            license = CommandLicense().run(folder)

            if license['valid'] != "1":

                message = license["error"]

                if license["error"].find("local issuer certificate") != -1:
                    message += ". You might be trying to upload a valid license key but for Web Safety version 5. Such keys are not supported. Please contact support@diladele.com to convert your valid license key to a new format."

                raise Exception(message)

        except Exception as e:            

            raise Exception("License key is invalid, error: %s" % str(e))

        # if we got here, then the license key is fine, replace the current one
        shutil.copy(
            os.path.join(folder, "license.pem"),
            os.path.join(Paths.etc_dir(), "license.pem")
        )

        # good, now if the license is community, activate/deactivate web safety
        self.activate_safety()