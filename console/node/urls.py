from django.views import generic
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from node.models import *
from node import views

urlpatterns = [

    # dash
    url(r'^$', views.ViewDashboard.as_view(), name='ViewDashboard'),

	# dash api
    url(r'^api/v1/dash/info/system$', views.ViewApiDashInfo.as_view(), name='ViewApiDashInfo'),
    url(r'^api/v1/dash/info/icap$',   views.ViewApiDashIcap.as_view(), name='ViewApiDashIcap'),
    url(r'^api/v1/dash/info/squid$',  views.ViewApiDashSquid.as_view(), name='ViewApiDashSquid'),
    url(r'^api/v1/dash/info/wsmgrd$', views.ViewApiDashWsmgrd.as_view(), name='ViewApiDashWsmgrd'),
    url(r'^api/v1/dash/info/mysql$',  views.ViewApiDashTraffic.as_view(), name='ViewApiDashTraffic'),
    url(r'^api/v1/dash/runtime/squid$',  views.ViewApiDashSquidRuntime.as_view(), name='ViewApiDashSquidRuntime'),

    
    # clustering
    url(r'^cluster/client/update$',     views.ViewClusterClient.as_view(), name='ViewClusterClient'),
    url(r'^cluster/server/update$',     views.ViewClusterServer.as_view(), name='ViewClusterServer'),
    url(r'^cluster/server/nodes/list$', views.ViewClusterServerNodesList.as_view(), name='ViewClusterServerNodesList'),
    url(r'^cluster/log$',               views.ViewClusterLog.as_view(), name='ViewClusterLog'),

    # timezone
    url(r'^system/timezone/update$', views.ViewTimeZone.as_view(), name='ViewTimeZone'),

    # hostname
    url(r'^system/hostname/update$', views.ViewHostName.as_view(), name='ViewHostName'),

    # network
    url(r'^system/network/device/list$', views.ViewNetworkDeviceList.as_view(), name='ViewNetworkDeviceList'),
    url(r'^system/network/device/(?P<pk>\w+)/ipv4/update$', views.ViewNetworkDeviceIpv4Update.as_view(), name='ViewNetworkDeviceIpv4Update'),
    url(r'^system/network/device/(?P<pk>\w+)/ipv6/update$', views.ViewNetworkDeviceIpv6Update.as_view(), name='ViewNetworkDeviceIpv6Update'),
    url(r'^system/network/manual/update$', views.ViewNetworkManual.as_view(), name='ViewNetworkManual'),

    url(r'^license$', views.ViewLicense.as_view(), name='ViewLicense'),    
    url(r'^tools/sharing$', views.ViewDataChoices.as_view(), name='ViewDataChoices'),
    url(r'^tools/backup/settings$', views.ViewBackUp.as_view(), name='ViewBackUp'),
    url(r'^tools/backup/tgz$', views.ViewBackUpDownloadTarGz.as_view(), name='ViewBackUpDownloadTarGz'),
    url(r'^tools/restore$', views.ViewRestore.as_view(), name='ViewRestore'),
]