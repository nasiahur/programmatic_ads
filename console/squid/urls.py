#
# django
#
from django.conf.urls import url

#
# our
#
from squid import views

#
#
#
urlpatterns = [

    # general
    url(
    	r'^general/config$', 
    	views.ViewGeneralConfig.as_view(), 
    	name='ViewGeneralConfig'
    ),
    url(
    	r'^general/parse$', 
    	views.ViewGeneralParse.as_view(), 
    	name='ViewGeneralParse'
    ),
    url(
    	r'^general/version$', 
    	views.ViewGeneralVersion.as_view(), 
    	name='ViewGeneralVersion'
    ),

    # runtime
    url(
        r'^runtime/mgrinfo$', 
        views.ViewRuntime.as_view(template_name="squid/general/mgrinfo.html"), 
        name='ViewRuntimeMgrInfo'
    ),
    url(
        r'^runtime/counters$', 
        views.ViewRuntime.as_view(template_name="squid/general/counters.html"), 
        name='ViewRuntimeCounters'
    ),
    url(
        r'^runtime/counters/min5$', 
        views.ViewRuntime.as_view(template_name="squid/general/5min.html"), 
        name='ViewRuntimeCountersMin5'
    ),
    url(
        r'^runtime/counters/min60$', 
        views.ViewRuntime.as_view(template_name="squid/general/60min.html"), 
        name='ViewRuntimeCountersMin60'
    ),
    url(
        r'^runtime/utilization$', 
        views.ViewRuntime.as_view(template_name="squid/general/utilization.html"), 
        name='ViewRuntimeUtilization'
    ),
    url(
        r'^runtime/dnsinfo$', 
        views.ViewRuntime.as_view(template_name="squid/general/dnsinfo.html"), 
        name='ViewRuntimeDnsInfo'
    ),
    url(
        r'^runtime/auth/negotiate$', 
        views.ViewRuntime.as_view(template_name="squid/general/auth_negotiate.html"), 
        name='ViewRuntimeAuthNegotiate'
    ),
    url(
        r'^runtime/auth/ntlm$', 
        views.ViewRuntime.as_view(template_name="squid/general/auth_ntlm.html"), 
        name='ViewRuntimeAuthNtlm'
    ),
    url(
        r'^runtime/auth/basic$', 
        views.ViewRuntime.as_view(template_name="squid/general/auth_basic.html"), 
        name='ViewRuntimeAuthBasic'
    ),
    url(
        r'^runtime/client/list$', 
        views.ViewRuntime.as_view(template_name="squid/general/client_list.html"), 
        name='ViewRuntimeClientList'
    ),
    url(
        r'^runtime/active/requests$', 
        views.ViewRuntime.as_view(template_name="squid/general/active_requests.html"), 
        name='ViewRuntimeActiveRequests'
    ),

    # settings
    url(r'^network/info/$', views.ViewNetworkInfo.as_view(), name='ViewNetworkInfo'),
    url(r'^acls/$', views.ViewAcls.as_view(), name='ViewAcls'),
    url(r'^administrative/$', views.ViewAdministrative.as_view(), name='ViewAdministrative'),
    url(r'^dns/$', views.ViewDns.as_view(), name='ViewDns'),
    url(r'^miscellaneous/$', views.ViewMiscellaneous.as_view(), name='ViewMiscellaneous'),
    
    # ssl
    url(r'^ssl/info$', views.ViewSslInfo.as_view(), name='ViewSslInfo'),
    url(r'^ssl/mode$', views.ViewSslMode.as_view(), name='ViewSslMode'),
    url(r'^ssl/der$', views.ViewSslDer.as_view(), name='ViewSslDer'),
    url(r'^ssl/pem/backup$', views.ViewSslPemBackUp.as_view(), name='ViewSslPemBackUp'),
    url(r'^ssl/pem/upload$', views.ViewSslPemUpload.as_view(), name='ViewSslPemUpload'),
    url(r'^ssl/pem/generate$', views.ViewSslPemGenerate.as_view(), name='ViewSslPemGenerate'),
    url(r'^ssl/target/domain/list$', views.ViewSslTargetDomainList.as_view(), name='ViewSslTargetDomainList'),
    url(r'^ssl/target/domain/create$', views.ViewSslTargetDomainCreate.as_view(), name='ViewSslTargetDomainCreate'),
    url(r'^ssl/target/domain/(?P<pk>\d+)/update$', views.ViewSslTargetDomainUpdate.as_view(), name='ViewSslTargetDomainUpdate'),
    url(r'^ssl/target/ip/list$', views.ViewSslTargetIpList.as_view(), name='ViewSslTargetIpList'),
    url(r'^ssl/target/ip/create$', views.ViewSslTargetIpCreate.as_view(), name='ViewSslTargetIpCreate'),
    url(r'^ssl/target/ip/(?P<pk>\d+)/update$', views.ViewSslTargetIpUpdate.as_view(), name='ViewSslTargetIpUpdate'),
    url(r'^ssl/target/subnet/list$', views.ViewSslTargetSubnetList.as_view(), name='ViewSslTargetSubnetList'),
    url(r'^ssl/target/subnet/create$', views.ViewSslTargetSubnetCreate.as_view(), name='ViewSslTargetSubnetCreate'),
    url(r'^ssl/target/subnet/(?P<pk>\d+)/update$', views.ViewSslTargetSubnetUpdate.as_view(), name='ViewSslTargetSubnetUpdate'),
    url(r'^ssl/error/domain/list$', views.ViewSslErrorDomainList.as_view(), name='ViewSslErrorDomainList'),
    url(r'^ssl/error/domain/create$', views.ViewSslErrorDomainCreate.as_view(), name='ViewSslErrorDomainCreate'),
    url(r'^ssl/error/domain/(?P<pk>\d+)/update$', views.ViewSslErrorDomainUpdate.as_view(), name='ViewSslErrorDomainUpdate'),
    url(r'^ssl/error/ip/list$', views.ViewSslErrorIpList.as_view(), name='ViewSslErrorIpList'),
    url(r'^ssl/error/ip/create$', views.ViewSslErrorIpCreate.as_view(), name='ViewSslErrorIpCreate'),
    url(r'^ssl/error/ip/(?P<pk>\d+)/update$', views.ViewSslErrorIpUpdate.as_view(), name='ViewSslErrorIpUpdate'),
    url(r'^ssl/error/subnet/list$', views.ViewSslErrorSubnetList.as_view(), name='ViewSslErrorSubnetList'),
    url(r'^ssl/error/subnet/create$', views.ViewSslErrorSubnetCreate.as_view(), name='ViewSslErrorSubnetCreate'),
    url(r'^ssl/error/subnet/(?P<pk>\d+)/update$', views.ViewSslErrorSubnetUpdate.as_view(), name='ViewSslErrorSubnetUpdate'),
    url(r'^ssl/missing/certs/list$', views.ViewSslIntermediateCertList.as_view(), name='ViewSslIntermediateCertList'),
    url(r'^ssl/missing/certs/create$', views.ViewSslIntermediateCertCreate.as_view(), name='ViewSslIntermediateCertCreate'),
    url(r'^ssl/missing/certs/backup$', views.ViewSslIntermediateCertBackUp.as_view(), name='ViewSslIntermediateCertBackUp'),

    # exclusions    
    url(r'^exclude/domain/name/list$',                 views.ViewExcludeDomainNameList.as_view(),     name='ViewExcludeDomainNameList'),
    url(r'^exclude/domain/name/create$',               views.ViewExcludeDomainNameCreate.as_view(),   name='ViewExcludeDomainNameCreate'),
    url(r'^exclude/domain/name/(?P<pk>\d+)/update$',   views.ViewExcludeDomainNameUpdate.as_view(),   name='ViewExcludeDomainNameUpdate'),
    url(r'^exclude/domain/ip/list$',                   views.ViewExcludeDomainIpList.as_view(),       name='ViewExcludeDomainIpList'),
    url(r'^exclude/domain/ip/create$',                 views.ViewExcludeDomainIpCreate.as_view(),     name='ViewExcludeDomainIpCreate'),
    url(r'^exclude/domain/ip/(?P<pk>\d+)/update$',     views.ViewExcludeDomainIpUpdate.as_view(),     name='ViewExcludeDomainIpUpdate'),
    url(r'^exclude/domain/range/list$',                views.ViewExcludeDomainRangeList.as_view(),    name='ViewExcludeDomainRangeList'),
    url(r'^exclude/domain/range/create$',              views.ViewExcludeDomainRangeCreate.as_view(),  name='ViewExcludeDomainRangeCreate'),
    url(r'^exclude/domain/range/(?P<pk>\d+)/update$',  views.ViewExcludeDomainRangeUpdate.as_view(),  name='ViewExcludeDomainRangeUpdate'),
    url(r'^exclude/domain/subnet/list$',               views.ViewExcludeDomainSubnetList.as_view(),   name='ViewExcludeDomainSubnetList'),
    url(r'^exclude/domain/subnet/create$',             views.ViewExcludeDomainSubnetCreate.as_view(), name='ViewExcludeDomainSubnetCreate'),
    url(r'^exclude/domain/subnet/(?P<pk>\d+)/update$', views.ViewExcludeDomainSubnetUpdate.as_view(), name='ViewExcludeDomainSubnetUpdate'),
    url(r'^exclude/user/ip/list$',                     views.ViewExcludeUserIpList.as_view(),         name='ViewExcludeUserIpList'),
    url(r'^exclude/user/ip/create$',                   views.ViewExcludeUserIpCreate.as_view(),       name='ViewExcludeUserIpCreate'),
    url(r'^exclude/user/ip/(?P<pk>\d+)/update$',       views.ViewExcludeUserIpUpdate.as_view(),       name='ViewExcludeUserIpUpdate'),
    url(r'^exclude/user/range/list$',                  views.ViewExcludeUserRangeList.as_view(),      name='ViewExcludeUserRangeList'),
    url(r'^exclude/user/range/create$',                views.ViewExcludeUserRangeCreate.as_view(),    name='ViewExcludeUserRangeCreate'),
    url(r'^exclude/user/range/(?P<pk>\d+)/update$',    views.ViewExcludeUserRangeUpdate.as_view(),    name='ViewExcludeUserRangeUpdate'),
    url(r'^exclude/user/subnet/list$',                 views.ViewExcludeUserSubnetList.as_view(),     name='ViewExcludeUserSubnetList'),
    url(r'^exclude/user/subnet/create$',               views.ViewExcludeUserSubnetCreate.as_view(),   name='ViewExcludeUserSubnetCreate'),
    url(r'^exclude/user/subnet/(?P<pk>\d+)/update$',   views.ViewExcludeUserSubnetUpdate.as_view(),   name='ViewExcludeUserSubnetUpdate'),    
    url(r'^exclude/user/agent/list$',                  views.ViewExcludeUserAgentList.as_view(),      name='ViewExcludeUserAgentList'),
    url(r'^exclude/user/agent/create$',                views.ViewExcludeUserAgentCreate.as_view(),    name='ViewExcludeUserAgentCreate'),
    url(r'^exclude/user/agent/(?P<pk>\d+)/update$',    views.ViewExcludeUserAgentUpdate.as_view(),    name='ViewExcludeUserAgentUpdate'),
    url(r'^exclude/content/type/list$',                views.ViewExcludeContentTypeList.as_view(),    name='ViewExcludeContentTypeList'),
    url(r'^exclude/content/type/create$',              views.ViewExcludeContentTypeCreate.as_view(),  name='ViewExcludeContentTypeCreate'),
    url(r'^exclude/content/type/(?P<pk>\d+)/update$',  views.ViewExcludeContentTypeUpdate.as_view(),  name='ViewExcludeContentTypeUpdate'),
    url(r'^exclude/schedule/list$',                    views.ViewExcludeScheduleList.as_view(),       name='ViewExcludeScheduleList'),
    url(r'^exclude/schedule/create$',                  views.ViewExcludeScheduleCreate.as_view(),     name='ViewExcludeScheduleCreate'),
    url(r'^exclude/schedule/(?P<pk>\d+)/update$',      views.ViewExcludeScheduleUpdate.as_view(),     name='ViewExcludeScheduleUpdate'),
    url(r'^exclude/advanced/ssl$',                     views.ViewExcludeAdvancedSsl.as_view(),        name='ViewExcludeAdvancedSsl'),    
    url(r'^exclude/advanced/adaptation$',              views.ViewExcludeAdvancedAdaptation.as_view(), name='ViewExcludeAdvancedAdaptation'),
    url(r'^exclude/advanced/auth$',                    views.ViewExcludeAdvancedAuth.as_view(),       name='ViewExcludeAdvancedAuth'),
    url(r'^exclude/advanced/cache$',                   views.ViewExcludeAdvancedCache.as_view(),      name='ViewExcludeAdvancedCache'),
    url(r'^exclude/advanced/urlrewriter$',             views.ViewExcludeAdvancedUrlRewriter.as_view(),name='ViewExcludeAdvancedUrlRewriter'),
    url(r'^exclude/category/update$',                  views.ViewExcludeCategoryUpdate.as_view(),     name='ViewExcludeCategoryUpdate'),

    # auth
    url(r'^auth/mode/explicit$', views.ViewAuthExplicit.as_view(), name='ViewAuthExplicit'),
    url(r'^auth/mode/pseudo$', views.ViewAuthPseudo.as_view(), name='ViewAuthPseudo'),
    url(r'^auth/domain/edit$', views.ViewAuthDomainEdit.as_view(), name='ViewAuthDomainEdit'),
    url(r'^auth/domain/test/$', views.ViewAuthDomainTest.as_view(), name='ViewAuthDomainTest'),    
    url(r'^auth/domain/ldaps$', views.ViewAuthDomainLdaps.as_view(), name='ViewAuthDomainLdaps'),
    url(r'^auth/domain/ldaps/export$', views.ViewAuthDomainLdapsExport.as_view(), name='ViewAuthDomainLdapsExport'),
    url(r'^auth/domain/ldaps/remove$', views.ViewAuthDomainLdapsRemove.as_view(), name='ViewAuthDomainLdapsRemove'),
    url(r'^auth/domain/ldaps/detect$', views.ViewLdapsDetect.as_view(), name='ViewLdapsDetect'),
    url(r'^auth/detect$', views.ViewAuthDetect.as_view(), name='ViewAuthDetect'),
    url(r'^auth/group/edit$', views.ViewAuthGroupMembershipEdit.as_view(), name='ViewAuthGroupMembershipEdit'),
    url(r'^auth/negotiate/scheme/edit$', views.ViewAuthNegotiateSchemeEdit.as_view(), name='ViewAuthNegotiateSchemeEdit'),
    url(r'^auth/negotiate/scheme/download/keytab$', views.ViewAuthNegotiateSchemeGetKeyTab.as_view(), name='ViewAuthNegotiateSchemeGetKeyTab'),
    url(r'^auth/ntlm/scheme/edit$', views.ViewAuthNtlmSchemeEdit.as_view(), name='ViewAuthNtlmSchemeEdit'),
    url(r'^auth/ldap/scheme/edit$', views.ViewAuthLdapSchemeEdit.as_view(), name='ViewAuthLdapSchemeEdit'),
    url(r'^auth/localdb/edit$', views.ViewAuthLocalDbEdit.as_view(), name='ViewAuthLocalDbEdit'),
    url(r'^auth/localdb/user/list/$', views.ViewAuthLocalDbUsersList.as_view(), name='ViewAuthLocalDbUsersList'),
    url(r'^auth/localdb/user/(?P<pk>[\w\.]+)/edit/$', views.ViewAuthLocalDbUsersUpdate.as_view(), name='ViewAuthLocalDbUsersUpdate'),
    url(r'^auth/localdb/user/create/$', views.ViewAuthLocalDbUsersCreate.as_view(), name='ViewAuthLocalDbUsersCreate'),
    url(r'^auth/localdb/export/$', views.ViewAuthLocalDbExport.as_view(), name='ViewAuthLocalDbExport'),
    url(r'^auth/localdb/import$', views.ViewAuthLocalDbImport.as_view(), name='ViewAuthLocalDbImport'),
    url(r'^auth/radius/edit$', views.ViewAuthRadiusEdit.as_view(), name='ViewAuthRadiusEdit'),
    
    url(r'^auth/label/edit$', views.ViewAuthLabelEdit.as_view(), name='ViewAuthLabelEdit'),
    url(r'^auth/label/user/list/$', views.ViewAuthLabelList.as_view(), name='ViewAuthLabelList'),
    url(r'^auth/label/user/(?P<pk>[\w\.]+)/edit/$', views.ViewAuthLabelUpdate.as_view(), name='ViewAuthLabelUpdate'),
    url(r'^auth/label/user/create/$', views.ViewAuthLabelCreate.as_view(), name='ViewAuthLabelCreate'),

    url(r'^auth/pseudo/edit$', views.ViewAuthPseudoEdit.as_view(), name='ViewAuthPseudoEdit'),
    url(r'^auth/pseudo/user/list/$', views.ViewAuthPseudoList.as_view(), name='ViewAuthPseudoList'),
    
    # tools
    url(r'^tools/upload$', views.ToolsUploadSquidFile.as_view(), name='ToolsUploadSquidFile'),
    url(r'^tools/wpad/upload$', views.ToolsUploadWpad.as_view(), name='ToolsUploadWpad'),
    url(r'^tools/wpad/remove$', views.ToolsRemoveWpad.as_view(), name='ToolsRemoveWpad'),
    url(r'^tools/sslservertest$', views.ToolsSslServerTest.as_view(), name='ToolsSslServerTest'),

    # logs
    url(r'^logs/access/log$', views.ViewAccessLog.as_view(), name='ViewAccessLog'),
    url(r'^logs/cache/log$', views.ViewCacheLog.as_view(), name='ViewCacheLog'),
    url(r'^logs/levels$', views.ViewLogLevels.as_view(), name='ViewLogLevels'),
    url(r'^logs/section/(?P<pk>\d+)/update$', views.ViewLogSectionUpdate.as_view(), name='ViewLogSectionUpdate'),

    # cache
    url(r'^cache/memory$', views.ViewCacheMemory.as_view(), name='ViewCacheMemory'),
    url(r'^cache/disk$', views.ViewCacheDisk.as_view(), name='ViewCacheDisk'),
    url(r'^cache/disk/enable/$', views.ViewCacheDiskEnable.as_view(), name='ViewCacheDiskEnable'),
    url(r'^cache/disk/reset/$', views.ViewCacheDiskReset.as_view(), name='ViewCacheDiskReset'),
    url(r'^cache/refresh/pattern/list$', views.ViewCacheRefreshPatternList.as_view(), name='ViewCacheRefreshPatternList'),
    url(r'^cache/refresh/pattern/create$', views.ViewCacheRefreshPatternCreate.as_view(), name='ViewCacheRefreshPatternCreate'),
    url(r'^cache/refresh/pattern/(?P<pk>\d+)/update$', views.ViewCacheRefreshPatternUpdate.as_view(), name='ViewCacheRefreshPatternUpdate'),
]