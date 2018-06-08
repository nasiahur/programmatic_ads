#
# business logic
#
from _domain.core import System, Distrib
from _domain.utils import LicenseManager

#
# django
#
from django.db import models

#
#
#
class Node(models.Model):   

    def can_manage_network(self):

        # for debug
        if System.WS_WINDOWS == System.name():
            return True

        if System.WS_LINUX == System.name():
            if Distrib.name() in [Distrib.WS_DEBIAN9, Distrib.WS_UBUNTU16]:
                return True

        return False

#
#
#
class NetManual(models.Model):

    value = models.TextField(blank=True)
    


#
#
#
class NetDevice(models.Model):

    CONFIG_TYPE_NONE     = 0
    CONFIG_TYPE_DHCP     = 1
    CONFIG_TYPE_STATIC   = 2
    #CONFIG_TYPE_LOOPBACK = 3
    #CONFIG_TYPE_MANUAL   = 4
    CONFIG_TYPE_CHOICES  = (
        (CONFIG_TYPE_NONE,     "None"),
        (CONFIG_TYPE_DHCP,     "DHCP"),
        (CONFIG_TYPE_STATIC,   "Static"),
        #(CONFIG_TYPE_LOOPBACK, "Loopback"),
        #(CONFIG_TYPE_MANUAL,   "Manual")
    )

    name    = models.CharField(max_length=64,  unique=True)
    mac     = models.CharField(max_length=128, blank=True)
    state   = models.CharField(max_length=16,  blank=True)

    # ip4
    ip4_config      = models.IntegerField(default=CONFIG_TYPE_DHCP,choices=CONFIG_TYPE_CHOICES)
    ip4_address     = models.CharField(max_length=254, blank=True)
    ip4_netmask     = models.CharField(max_length=254, blank=True)
    ip4_gateway     = models.CharField(max_length=254, blank=True)
    ip4_dns_srv1    = models.CharField(max_length=254, blank=True)
    ip4_dns_srv2    = models.CharField(max_length=254, blank=True)
    ip4_dns_search  = models.CharField(max_length=254, blank=True)

    def ip4_config_type_etc_network_interfaces_str(self):

        if NetDevice.CONFIG_TYPE_DHCP == self.ip4_config:
            return "dhcp"
        if NetDevice.CONFIG_TYPE_STATIC == self.ip4_config:
            return "static"
        #if NetDevice.CONFIG_TYPE_LOOPBACK == self.ip4_config:
        #    return "loopback"
        #if NetDevice.CONFIG_TYPE_MANUAL == self.ip4_config:
        #    return "manual"
        return "none"


    # ip6
    ip6_config      = models.IntegerField(default=CONFIG_TYPE_NONE,choices=CONFIG_TYPE_CHOICES)
    ip6_address     = models.CharField(max_length=254, blank=True)
    ip6_subnet      = models.IntegerField(default=64)
    ip6_gateway     = models.CharField(max_length=254, blank=True)
    ip6_dns_srv1    = models.CharField(max_length=254, blank=True)
    ip6_dns_srv2    = models.CharField(max_length=254, blank=True)
    ip6_dns_search  = models.CharField(max_length=254, blank=True)

    def ip6_config_type_etc_network_interfaces_str(self):

        if NetDevice.CONFIG_TYPE_DHCP == self.ip6_config:
            return "dhcp"
        if NetDevice.CONFIG_TYPE_STATIC == self.ip6_config:
            return "static"
        #if NetDevice.CONFIG_TYPE_LOOPBACK == self.ip6_config:
        #    return "loopback"
        #if NetDevice.CONFIG_TYPE_MANUAL == self.ip6_config:
        #    return "manual"
        return "none"

    def __str__(self):
        return self.name


#
#
#
class Sharing(models.Model):
    
    upload_recategorization   = models.BooleanField(default=False)
    upload_telemetry_basic    = models.BooleanField(default=False)
    upload_telemetry_extended = models.BooleanField(default=False)
