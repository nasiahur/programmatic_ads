from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include

from squid.views import AutoProxyDiscoverView
admin.autodiscover()

urlpatterns = [
    url(r'^accounts/login/$',   login, {'template_name': 'login.html'}, name="LoginView"),
    url(r'^accounts/logout/$',  logout, {'template_name': 'logged_out.html'}, name="LogoutView"),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('node:ViewDashboard'), permanent=False)),
    url(r'^frame/', include('frame.urls', namespace='frame')),    
    url(r'^node/', include('node.urls', namespace='node')),
    url(r'^safety/', include('safety.urls')),    
    url(r'^squid/', include('squid.urls')),    
    url(r'^antivirus/', include('antivirus.urls')),    
    url(r'^traffic/', include('traffic.urls', namespace='traffic')),
    url(r'^wpad.dat?$', AutoProxyDiscoverView.as_view(), name="AutoProxyDiscoverView"),
    url(r'^proxy.pac$', AutoProxyDiscoverView.as_view(), name="AutoProxyDiscoverView"),    
    url(r'^admin/', include(admin.site.urls)),
]