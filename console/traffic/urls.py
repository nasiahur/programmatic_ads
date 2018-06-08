#
# django
#
from django.conf.urls import url

#
# our
#
from traffic import views


urlpatterns = [

    # templates
    url(r'^templates/list/$', views.ViewReportTemplates.as_view(), name='ViewReportTemplates'),        
    
    # jobs
    url(r'^jobs/list/$', views.ViewReportJobs.as_view(), name='ViewReportJobs'),        
    url(r'^jobs/create/(?P<template>[\w\-]+)/$', views.ViewReportCreateJob.as_view(), name='ViewReportCreateJob'),        
    url(r'^jobs/(?P<pk>\d+)/(?P<template>[\w\-]+)/edit/$', views.ViewReportUpdateJob.as_view(), name='ViewReportUpdateJob'),        
    url(r'^jobs/(?P<pk>\d+)/generate/$', views.ViewReportGenerateJob.as_view(), name='ViewReportGenerateJob'),

    # report viewer
    url(r'^jobs/(?P<name>[\w\- ]+)/view/(?P<file>.*)$', views.ViewReportViewJob.as_view(), name='ViewReportViewJob'),

    # report exporter
    url(r'^jobs/(?P<name>[\w\- ]+)/exportpdf/$', views.ViewReportExportPdf.as_view(), name='ViewReportExportPdf'),

    # monitoring
    url(r'^monitor/surfing/now/$', views.View_MonitorSurfingNow.as_view(), name='View_MonitorSurfingNow'),
    url(r'^monitor/incident/$', views.View_MonitorIncidentList.as_view(), name='View_MonitorIncidentList'),
    url(r'^monitor/incident/(?P<pk>\d+)/$', views.View_MonitorIncident.as_view(), name='View_MonitorIncident'),
    url(r'^monitor/update/globals/$', views.View_MonitoringUpdateGlobals.as_view(), name='View_MonitoringUpdateGlobals'),    
    url(r'^monitor/update/channels/$', views.View_MonitoringUpdateChannels.as_view(), name='View_MonitoringUpdateChannels'),    
    url(r'^monitor/update/smtpconnector/$', views.View_MonitoringUpdateSmtpConnector.as_view(), name='View_MonitoringUpdateSmtpConnector'),    
    url(r'^monitor/update/advanced/$', views.View_MonitoringUpdateAdvanced.as_view(), name='View_MonitoringUpdateAdvanced'),    
    url(r'^monitor/info/$', views.View_MonitorInfo.as_view(), name='View_MonitorInfo'),
    url(r'^monitor/monitor_log/$', views.View_MonitorUploadLog.as_view(), name='View_MonitorUploadLog'),
    url(r'^monitor/database_log/$', views.View_MonitorDatabaseLog.as_view(), name='View_MonitorDatabaseLog'),


]