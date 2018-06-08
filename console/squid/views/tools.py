#
#
#
import os
import traceback

#
#
#
from django import forms
from django.views import generic
from django.conf  import settings
from django.http  import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

#
# domain logic (non django)
#
from _domain.squid import CertChainCollector, CertChainVerifier, CertChainResolver


#
# squid tools form
#
IMPORT_FILE_CHOICES = (

    # exclusions
    ('ExcludeDomainName',   'Exclude Domain Name'),
    ('ExcludeDomainIp',     'Exclude Domain IP'),
    ('ExcludeDomainSubnet', 'Exclude Domain Subnet'),
    ('ExcludeDomainRange',  'Exclude Domain Range'),    
    ('ExcludeUserIp',       'Exclude User Ip'),    
    ('ExcludeUserSubnet',   'Exclude User Subnet'),
    ('ExcludeUserRange',    'Exclude User Range'),
    ('ExcludeUserAgent',    'Exclude User Agent'),
    ('ExcludeContentType',  'Exclude Content Type'),    
    ('SslTargetDomain',     'Ssl Target Domain'),
    ('SslTargetIp',         'Ssl Target IP Address'),
    ('SslTargetSubnet',     'Ssl Target IP Subnet'),
    ('SslErrorDomain',      'Ssl Error Domain'),
    ('SslErrorIp',          'Ssl Error IP Address'),
    ('SslErrorSubnet',      'Ssl Error IP Subnet'),
)



#
#
#
class UploadFileForm(forms.Form):

    file    = forms.FileField()
    type    = forms.ChoiceField(choices=IMPORT_FILE_CHOICES)
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )


#
# squid tools
#    
class ToolsUploadSquidFile(generic.View):

    def get(self, request, *args, **kwargs):
        return render(request, 'squid/tools/upload.html', {'form': UploadFileForm() })

    def collect(self, data):

        collected = ""
        for chunk in data.chunks():
            collected += chunk

        result = []
        array  = collected.split('\n')
        for line in array:
            line = line.strip('\n')
            line = line.strip('\r')
            line = line.strip(' ')

            if len(line) > 0:
                result.append(line)    

        return result

    def drop_comments(self, items):

        result = []
        for item in items:
            pos = item.find("#")
            if pos != -1:
                item = item[:pos].strip()
            if len(item) > 0:
                result.append(item)            
        return result

    def import_file(self, model_name, array, comment):

        from django.apps import apps

        model = apps.get_model("squid.%s" % model_name)
        query = model.objects

        for item in array:
            found = query.filter(value__exact=item)
            if len(found) > 0:
                continue
            
            new_entry = model(value=item)
            try:
                new_entry.comment = comment
            except Exception as e:
                pass

            new_entry.save()

    def post(self, request, *args, **kwargs):

        # get the form
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'squid/tools/upload.html', {'form': form })

        # try to import and redisplay if failed
        try:

            # process data
            array = []
            if 'file' in self.request.FILES:
                array = self.collect(self.request.FILES['file'])

            # drop all comments
            array = self.drop_comments(array)

            # get comment in form
            comment = form.cleaned_data.get('comment', '')

            # see if we need to import squid or policy
            self.import_file(form.cleaned_data['type'], array, comment)
            
        except Exception as e:
            return render(request, 'squid/tools/upload.html', {'form': form, 'error': str(e), 'stack': traceback.format_exc() })

        # mark as needing reload
        messages.info(self.request, "need_squid_restart")

        # and redirect
        return HttpResponseRedirect(reverse_lazy("ToolsUploadSquidFile"))



#
#
#
class SslServerTestForm(forms.Form):
    
    server_name = forms.CharField()
    
    def clean_server_name(self):
        
        value = self.cleaned_data['server_name']
        value = value.strip()

        return value

class ToolsSslServerTest(generic.View):

    template_name = 'squid/tools/sslservertest.html'
    
    def get(self, request, *args, **kwargs):

        # get the form
        form    = SslServerTestForm(request.GET)
        error   = ""
        stack   = ""
        certs   = []
        server  = ""
        missing = False
        
        # see if we have something in get params
        try:
            if form.is_valid():
                
                # save the server name for template rendering
                server = form.cleaned_data['server_name']

                # get the certs
                certs = CertChainCollector(server).collect()

                # now try to verify the certificates
                (verify, err1) = CertChainVerifier(server).verify(certs)

                # if default verification fails
                if not verify:

                    # try to resolve missing certificates (note how we overwrite the certs with returned value!)
                    certs = CertChainResolver().resolve(certs)
                    
                    # and then verify again
                    (verify, err2) = CertChainVerifier(server).verify(certs)
                    if not verify:
                        raise Exception(
                            "Cannot verify list of certificates provided by the server! Error when verifying as is: %s;"
                            "Error when verifying after download of missing certificates: %s." % (err1, err2)
                        )

                    # see if at least one cert was downloaded
                    for cert in certs:
                        if cert.is_missing():
                            missing = True

        except Exception as e:
            error = str(e)
            stack = traceback.format_exc()

        # and render it again
        return render(request, self.template_name, {
            'form': form, 'server': server, 'error': error, 'stack': stack, 'certs': certs, 'missing': missing
        })