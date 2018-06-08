#
# django
#
from django.contrib import admin

#
# ours
#
from node.models import *

#
#
#
admin.site.register(Node)

class NetDeviceAdmin(admin.ModelAdmin):    
    list_display = ('name', 'mac', 'state', 'ip4_config', 'ip4_address', 'ip4_netmask', 'ip4_gateway', 'ip4_dns_srv1', 'ip4_dns_srv2', 'ip4_dns_search')

admin.site.register(NetDevice, NetDeviceAdmin)

