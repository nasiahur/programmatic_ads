#
# django
#
from django.conf.urls import url

#
# ours
#
from antivirus import views

#
# routes
#
urlpatterns = [

    # settings
    url(r'^settings/mode$', views.ViewAvSettingsMode.as_view(), name='ViewAvSettingsMode'),    
    url(r'^settings/ecap/actions$', views.ViewAvSettingsEcapActions.as_view(), name='ViewAvSettingsEcapActions'),    
    url(r'^settings/ecap/trickling$', views.ViewAvSettingsEcapTrickling.as_view(), name='ViewAvSettingsEcapTrickling'),    
    
    url(r'^settings/icap$', views.ViewAvSettingsIcap.as_view(), name='ViewAvSettingsIcap'),    

    # safe browsing
    url(r'^safebrowsing/edit$', views.ViewSafeBrowsingEdit.as_view(), name='ViewSafeBrowsingEdit'),    
    url(r'^safebrowsing/helpers$', views.ViewSafeBrowsingHelpers.as_view(), name='ViewSafeBrowsingHelpers'),    
    url(r'^safebrowsing/status$', views.ViewSafeBrowsingStatus.as_view(), name='ViewSafeBrowsingStatus'),    
    url(r'^safebrowsing/log$', views.ViewSafeBrowsingLog.as_view(), name='ViewSafeBrowsingLog'),    

    # blocked page (excluded from authentication!)
    url(r'^safebrowsing/blocked$', views.ViewSafeBrowsingBlocked.as_view(), name='ViewSafeBrowsingBlocked'),    
]