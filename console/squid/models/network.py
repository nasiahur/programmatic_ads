from django.db import models

#
#
#
class Network(models.Model):

    # explicit proxy is ALWAYS enabled (this is squid limitation not ours)
    explicit_address   = models.CharField(max_length=200, default="", blank=True) 
    explicit_port      = models.IntegerField(default=3128)

    # proxy protocol support (load balancing)
    enable_proxy_proto = models.BooleanField(default=False)
    proxy_hosts        = models.CharField(max_length=200, default="", blank=True)  # list of IP addresses of load balancers supplying PROXY header

    # intercept proxy configuration
    INTERCEPT_MODE_NONE    = 0
    INTERCEPT_MODE_WCCP    = 1
    INTERCEPT_MODE_GTW     = 2
    INTERCEPT_MODE_CHOICES = (
    	(INTERCEPT_MODE_NONE, "Not Configured / Disabled"), 
    	(INTERCEPT_MODE_WCCP, "Cisco WCCP Redirect"), 
    	(INTERCEPT_MODE_GTW, "Default Gateway Proxy"),
    )

    intercept_mode       = models.IntegerField(choices=INTERCEPT_MODE_CHOICES,default=INTERCEPT_MODE_NONE)
    intercept_address    = models.CharField(max_length=200, default="", blank=True) 
    intercept_port_http  = models.IntegerField(default=3126)
    intercept_port_https = models.IntegerField(default=3127)

    # used when intercept_mode == INTERCEPT_MODE_WCCP    
    wccp2_router         = models.CharField(max_length=200, default="", blank=True)
    wccp2_password       = models.CharField(max_length=200, default="", blank=True)
    
    def wccp2_conf_sample(self):

        sample = ""

        try:
            from django.template import loader, Context

            t = loader.get_template("squid/conf/wccp.conf")
            c = { "network": self }

            lines = t.render(c).split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("#") or len(line) == 0:
                    continue                
                sample += line + "\n"

        except Exception as e:
            sample = "ERROR:" + str(e)

        return sample

    def network_conf_sample(self):

        sample = ""

        try:
            from django.template import loader, Context

            t = loader.get_template("squid/conf/network.conf")
            c = {"network": self }

            lines = t.render(c).split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("#") or len(line) == 0:
                    continue                
                sample += line + "\n"

        except Exception as e:
            sample = "ERROR:" + str(e)

        return sample