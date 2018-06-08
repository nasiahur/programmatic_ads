import os
import json

#
# business logic
#
from _domain.core import Paths
from _domain.utils import FileWriter, JsonDumper
from _domain.node import SyncLog, ClusterServerNodesList


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
# cluster
#
class ClusterClientForm(forms.Form):

    enabled        = forms.BooleanField(required=False)
    server_address = forms.CharField(max_length=254, required=False)
    server_port    = forms.IntegerField(widget=forms.TextInput())
    sync_interval  = forms.IntegerField(widget=forms.TextInput())

    def clean(self):

        # get cleaned data
        cleaned_data = super(ClusterClientForm, self).clean()

        # we cannot enable if server address is empty
        enabled = cleaned_data.get('enabled', False)
        if enabled:
            server_address = cleaned_data.get('server_address')
            if len(server_address) == 0:
                self.errors['__all__'] = self.error_class(["Cannot activate configuration client functionality because server address is not set."])            
                raise forms.ValidationError("")

        return cleaned_data 

    
    def clean_enabled(self):

        enabled = self.cleaned_data['enabled']
        if enabled:
            
            # ok admin wants to enable client, let's see we are NOT server already
            name = os.path.join(Paths.etc_dir(), "node", "cluster_server.json")
            with open(name) as fin:    
                data = json.load(fin)

                if data['enabled']:
                    self.errors['__all__'] = self.error_class(["Cannot activate configuration client functionality because this node is already activated as configuration server."])            
                    raise forms.ValidationError("")

        return enabled

    def clean_sync_interval(self):

        value = self.cleaned_data['sync_interval']
        if value < 1:
            raise forms.ValidationError("Must be >= 1 second; recommended value is 5.")
        return value

    def clean_server_port(self):

        value = self.cleaned_data['server_port']
        if value < 1024 or value > 65534:
            raise forms.ValidationError("Must be within (1024:65535) interval; default value is 18999.")
        return value

#
#
#
class ViewClusterClient(SuccessMessageMixin, generic.View):

    template_name   = "node/cluster/client_form.html"
    success_message = "need_squid_restart"
    form_class      = ClusterClientForm

    def get_success_url(self):
        return reverse_lazy('node:ViewClusterClient')

    def get(self, request, *args, **kwargs):

        data = {}
        name = os.path.join(Paths.etc_dir(), "node", "cluster_client.json")
        if os.path.exists(name):
            with open(name) as fin:    
                data = json.load(fin)

        form = ClusterClientForm(initial=data)

        return render(request, self.template_name, {'form': form })

    def post(self, request, *args, **kwargs):

        form  = ClusterClientForm(request.POST)
        if form.is_valid():

            # ok form is valid, fill the data
            data = {
                "enabled"       : form.cleaned_data['enabled'], 
                "server_port"   : form.cleaned_data['server_port'], 
                "server_address": form.cleaned_data['server_address'], 
                "sync_interval" : form.cleaned_data['sync_interval']
            }

            # and write it
            w = FileWriter(os.path.join(Paths.etc_dir(), "node"))
            d = JsonDumper()

            w.write('cluster_client.json', d.dumps(data))

            # mark as needing relstart
            messages.info(request, "need_squid_restart")

            return HttpResponseRedirect(self.get_success_url()) 

        return render(request, self.template_name, {'form': form })

#
#
#
class ClusterServerForm(forms.Form):

    enabled        = forms.BooleanField(required=False)
    listen_address = forms.CharField(max_length=254, required=False)
    listen_port    = forms.IntegerField(widget=forms.TextInput())

    def clean_enabled(self):

        enabled = self.cleaned_data['enabled']
        if enabled:
            
            # ok admin wants to enable server, let's see we are NOT client already
            name = os.path.join(Paths.etc_dir(), "node", "cluster_client.json")
            with open(name) as fin:    
                data = json.load(fin)

                if data['enabled']:
                    self.errors['__all__'] = self.error_class(["Cannot activate configuration server functionality because this node is already activated as configuration client."])            
                    raise forms.ValidationError("")

        return enabled

    def clean_listen_port(self):

        value = self.cleaned_data['listen_port']
        if value < 1024 or value > 65534:
            raise forms.ValidationError("Must be within (1024:65535) interval; default value is 18999.")
        return value

#
#
#
class ViewClusterServer(SuccessMessageMixin, generic.View):

    template_name   = "node/cluster/server_form.html"
    success_message = "need_squid_restart"
    form_class      = ClusterClientForm

    def get_success_url(self):
        return reverse_lazy('node:ViewClusterServer')

    def get(self, request, *args, **kwargs):

        data = {}
        name = os.path.join(Paths.etc_dir(), "node", "cluster_server.json")
        if os.path.exists(name):
            with open(name) as fin:    
                data = json.load(fin)

        form = ClusterServerForm(initial=data)

        return render(request, self.template_name, {'form': form })

    def post(self, request, *args, **kwargs):

        form  = ClusterServerForm(request.POST)
        if form.is_valid():

            # ok form is valid, fill the data
            data = {
                "enabled"       : form.cleaned_data['enabled'], 
                "listen_port"   : form.cleaned_data['listen_port'], 
                "listen_address": form.cleaned_data['listen_address']
            }

            # and write it
            w = FileWriter(os.path.join(Paths.etc_dir(), "node"))
            d = JsonDumper()

            w.write('cluster_server.json', d.dumps(data))

            # mark as needing relstart
            messages.info(request, "need_squid_restart")

            return HttpResponseRedirect(self.get_success_url()) 

        return render(request, self.template_name, {'form': form })

#
#
#
class ViewClusterLog(generic.TemplateView):

    template_name = "node/cluster/sync_log.html"

    def get_context_data(self, **kwargs):
        context = super(ViewClusterLog, self).get_context_data(**kwargs)
        context['sync_log'] = SyncLog().get()
        return context

#
#
#
class ViewClusterServerNodesList(generic.TemplateView):

    template_name = "node/cluster/nodes.html"

    def get_context_data(self, **kwargs):
        
        context = super(ViewClusterServerNodesList, self).get_context_data(**kwargs)

        # allocate default response
        data = { 
            'error' : False,  
            'desc'  : '',  
            'items' : {} 
        }
        
        try:
            # get the wssyncd port for the REST service
            wsport = 18889
            
            name = os.path.join(Paths.etc_dir(), "node", "wssyncd.json")
            with open(name) as fin:    
                wssyncd = json.load(fin)
                wsport  = wssyncd['rest_service']['port']

            # see if server is enabled
            name = os.path.join(Paths.etc_dir(), "node", "cluster_server.json")
            with open(name) as fin:    
                cluster = json.load(fin)
                print(cluster)

                if cluster['enabled']:
                    data['items'] = ClusterServerNodesList().run(wsport)
            
        except Exception as e:
            data['error'] = True
            data['desc']  = str(e)
        
        context['nodes'] = data

        return context