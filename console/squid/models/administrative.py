from django.db import models

#
#
#
class Administrative(models.Model):

    cache_mgr = models.CharField(max_length=200, default="webmaster", blank=True) 
    #NOT_MANAGED: mail_from
    #NOT_MANAGED: mail_program
    #NOT_MANAGED: cache_effective_user
    #NOT_MANAGED: cache_effective_group
    httpd_suppress_version_string = models.BooleanField(default=False)
    visible_hostname              = models.CharField(max_length=200, default="proxy.example.lan", blank=True) 
    #NOT_MANAGED: unique_hostname
    #NOT_MANAGED: hostname_aliases
    #NOT_MANAGED: umask