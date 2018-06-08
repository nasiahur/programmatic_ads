from django.db import models

#
#
#
class Dns(models.Model):

    #NOT_MANAGED: check_hostnames
    #NOT_MANAGED: allow_underscore
    #NOT_MANAGED: dns_retransmit_interval
    dns_timeout     = models.IntegerField(default=30)
    #NOT_MANAGED: dns_packet_max
    #NOT_MANAGED: dns_defnames
    #NOT_MANAGED: dns_multicast_local
    dns_nameservers = models.CharField(max_length=200, default="", blank=True) 
    #NOT_MANAGED: hosts_file
    #NOT_MANAGED: append_domain
    #NOT_MANAGED: ignore_unknown_nameservers
    dns_v4_first    = models.BooleanField(default=True)
    #NOT_MANAGED: ipcache_size
    #NOT_MANAGED: ipcache_low
    #NOT_MANAGED: ipcache_high
    #NOT_MANAGED: fqdncache_size
