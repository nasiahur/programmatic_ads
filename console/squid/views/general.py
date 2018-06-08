import os
import json
import platform

#
# domain logic (non django)
#
from _domain.core import Paths
from _domain.squid import SquidConf, SquidParse, SquidClient, SquidVersion, BinarySquid


#
#
#
from django.views import generic

#
#
#
from squid.models import Network

#
#
#
class ViewGeneralConfig(generic.base.TemplateView):

    template_name = "squid/general/config.html"

    def get_context_data(self, **kwargs):
        
        context = super(ViewGeneralConfig, self).get_context_data(**kwargs)                
        context['conf']  = SquidConf()
        return context

#
#
#
class ViewGeneralParse(generic.base.TemplateView):

    template_name = "squid/general/parse.html"

    def get_context_data(self, **kwargs):
        
        context = super(ViewGeneralParse, self).get_context_data(**kwargs)        
        context['parse'] = SquidParse()
        
        return context

#
#
#
class ViewGeneralVersion(generic.base.TemplateView):

    template_name = "squid/general/version.html"

    def is_sslbump_capable(self):

        # debug
        if platform.platform().lower().startswith('windows'):
            return True

        # test for presence of specific flags in the squid version
        version_str = SquidVersion().get_str()
        if "--enable-ssl" in version_str:
            if "--enable-ssl-crtd" in version_str:
                return True

        return False

    def get_context_data(self, **kwargs):

        context = super(ViewGeneralVersion, self).get_context_data(**kwargs)        
        context['version'] = SquidVersion()
        context['sslbump_capable'] = self.is_sslbump_capable()
        
        return context

#
#
#
class ViewRuntime(generic.base.TemplateView):

    def get_context_data(self, **kwargs):

        # squid client needs to know what host and port to connect to
        network = Network.objects.first()

        # get and assign context
        context = super(ViewRuntime, self).get_context_data(**kwargs)        
        context['client']  = SquidClient(network.explicit_address, network.explicit_port)

        return context

#
#
#
class ViewRuntimeActiveRequests(generic.base.TemplateView):

    template_name="squid/general/active_requests.html"

    def get_context_data(self, **kwargs):

        # squid client needs to know what host and port to connect to
        network = Network.objects.first()
        client  = SquidClient(network.explicit_address, network.explicit_port)

        # get and assign context
        context = super(ViewRuntimeActiveRequests, self).get_context_data(**kwargs)        
        context['client']  = client
        
        return context
