import os
import json

#
# business logic
#
from _domain.core import Paths
from _domain.utils import LicenseManager

#
#
#
from django.views import generic

#
#
#
class ViewDashboard(generic.TemplateView):

    template_name = "node/dash/dash.html"

    def get_context_data(self, **kwargs):
        
        context = super(ViewDashboard, self).get_context_data(**kwargs)

        (result, license) = LicenseManager().get()
        if result is True:
            context['license'] = license

        is_cluster_client = False
        master_server     = ""

        # see if we are cluster client
        name = os.path.join(Paths.etc_dir(), "node", "cluster_client.json")
        if os.path.exists(name):
            with open(name) as fin:    
                data = json.load(fin)
                if data['enabled']:
                    is_cluster_client = True
                    master_server     = data['server_address']

        context['is_cluster_client'] = is_cluster_client
        context['master_server']     = master_server

        return context
