import os

#
#
#
from _domain.core import Paths



#
#
#
from django import forms
from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.http  import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

#
#
#
class AutoProxyDiscoverView(generic.View):

    def get(self, request, *args, **kwargs):            

        path = os.path.join(Paths.etc_dir(), "wpad.dat")
        with open(path, "rb") as fin:
            response = HttpResponse(fin.read(), content_type="application/x-ns-proxy-autoconfig")
            return response

#
#
#
class ToolsRemoveWpad(generic.View):

    def get(self, request, *args, **kwargs):
        wpad_dat = ""
        try:
            path = os.path.join(Paths.etc_dir(), "wpad.dat")
            os.unlink(path)
        except Exception as e:
            pass

        return HttpResponseRedirect(reverse_lazy("ToolsUploadWpad"))

#
# wpad form
#
class WpadUploadForm(forms.Form):
    file = forms.FileField()

#
#
#
class ToolsUploadWpad(generic.View):

    def get(self, request, *args, **kwargs):
        wpad_dat = ""
        try:
            path = os.path.join(Paths.etc_dir(), "wpad.dat")
            with open(path, "rb") as fin:
                wpad_dat = fin.read()
        except Exception as e:
            wpad_dat = str(e)

        return render(request, 'squid/tools/wpad.html', {'form': WpadUploadForm(), 'wpad_dat' : wpad_dat })

    def collect(self, data):

        collected = ""
        for chunk in data.chunks():
            collected += chunk

        return collected

    def store_file(self, contents):

        with open(os.path.join(Paths.etc_dir(), "wpad.dat"), 'wb') as fout:
            fout.write(contents)

    def post(self, request, *args, **kwargs):

        # get the form
        form = WpadUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'squid/tools/wpad.html', {'form': form })

        try:
            contents = ""
            if 'file' in self.request.FILES:
                contents = self.collect(self.request.FILES['file'])

            # see if we need to import squid or policy
            self.store_file(contents)
            
        except Exception as e:
            return render(request, 'squid/tools/wpad.html', {'form': form, 'error': str(e) })

        # mark as needing reload
        messages.info(self.request, "need_squid_reload")

        # and redirect
        return HttpResponseRedirect(reverse_lazy("ToolsUploadWpad"))
