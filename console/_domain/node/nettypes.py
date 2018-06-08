#
#
#
CONFIG_TYPE_NONE     = 0
CONFIG_TYPE_DHCP     = 1
CONFIG_TYPE_STATIC   = 2
#CONFIG_TYPE_LOOPBACK = 3
#CONFIG_TYPE_MANUAL   = 4
    
class ActualNetDeviceIp4:

    def __init__(self):
    
        self.config_type = CONFIG_TYPE_NONE
        self.address     = ""
        self.netmask     = ""
        self.gateway     = ""
        self.dns_srv1    = ""
        self.dns_srv2    = ""
        self.dns_search  = ""

class ActualNetDeviceIp6:

    def __init__(self):
    
        self.config_type = CONFIG_TYPE_NONE
        self.address     = ""
        self.subnet      = 64
        self.gateway     = ""
        self.dns_srv1    = ""
        self.dns_srv2    = ""
        self.dns_search  = ""

class ActualNetDevice:

    def __init__(self):

        self.name   = ""
        self.mac    = ""
        self.state  = ""
        self.ip4    = ActualNetDeviceIp4()
        self.ip6    = ActualNetDeviceIp6()


