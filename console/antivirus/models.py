#
# django
#
from django.db import models

#
#
#
class AvSettings(models.Model):
    
    enable             = models.BooleanField(default=False)
    bypass_to_localnet = models.BooleanField(default=True)                 # connections to hosts in our LAN does not need to be filtered

    AV_TYPE_ECAP_CLAMAV = 0
    AV_TYPE_AV_OTHER    = 1
    AV_TYPE_CHOICES = (
        (AV_TYPE_ECAP_CLAMAV, "eCAP ClamAV Antivirus Module"),
        (AV_TYPE_AV_OTHER,    "Third Party ICAP Antivirus Server")
    )
    av_type = models.IntegerField(default=AV_TYPE_ECAP_CLAMAV,choices=AV_TYPE_CHOICES)

    # eCAP ClamAV settings
    ECAP_CLAMAV_ERROR_ACTION_ALLOW = 0
    ECAP_CLAMAV_ERROR_ACTION_DENY  = 1
    ECAP_CLAMAV_ERROR_ACTION_CHOICES = (
        (ECAP_CLAMAV_ERROR_ACTION_ALLOW, "Allow Object"),
        (ECAP_CLAMAV_ERROR_ACTION_DENY,  "Deny Object")
    )

    ECAP_CLAMAV_TRICKLING_TYPE_HEADERS_ONLY     = 0
    ECAP_CLAMAV_TRICKLING_TYPE_HEADERS_AND_BODY = 1
    ECAP_CLAMAV_TRICKLING_TYPE_ALL              = 2
    ECAP_CLAMAV_TRICKLING_TYPE_CHOICES = (
        (ECAP_CLAMAV_TRICKLING_TYPE_HEADERS_ONLY,     "Trickle only headers"),
        (ECAP_CLAMAV_TRICKLING_TYPE_HEADERS_AND_BODY, "Trickle headers and limited body"),
        (ECAP_CLAMAV_TRICKLING_TYPE_ALL,              "Trickle everything")
    )

    ecap_clamav_async                 = models.BooleanField(default=False)
    ecap_clamav_message_size_max      = models.IntegerField(default=10485760)           # 10Mb
    ecap_clamav_on_error_action       = models.IntegerField(default=ECAP_CLAMAV_ERROR_ACTION_ALLOW,choices=ECAP_CLAMAV_ERROR_ACTION_CHOICES)
    #ecap_clamav_staging_dir           = models.CharField(max_length=254, blank=True)
    ecap_clamav_trickling_enable      = models.BooleanField(default=False)
    ecap_clamav_trickling_drop_size   = models.IntegerField(default=10)
    ecap_clamav_trickling_period      = models.IntegerField(default=10)                 # default is 10.0 seconds
    ecap_clamav_trickling_type        = models.IntegerField(default=ECAP_CLAMAV_TRICKLING_TYPE_HEADERS_AND_BODY,choices=ECAP_CLAMAV_TRICKLING_TYPE_CHOICES)
    ecap_clamav_trickling_size_max    = models.IntegerField(default=5242880)
    ecap_clamav_trickling_start_delay = models.IntegerField(default=1)                  # default is 1.0 second
    ecap_reqmod_bypass                = models.BooleanField(default=True)
    ecap_respmod_bypass               = models.BooleanField(default=True)

    # icap settings
    avicap_address    = models.CharField(max_length=200, default="127.0.0.1") # address of ICAP server for antivirus
    avicap_port       = models.IntegerField(default=1345)                     # port
    avicap_reqpath    = models.CharField(max_length=200, default="av_scan")   # request path
    avicap_respath    = models.CharField(max_length=200, default="av_scan")   # response path
    avicap_res_bypass = models.BooleanField(default=False)                    # if true ICAP errors are bypassed on AV RESPMOD filtering
    avicap_options    = models.TextField(blank=True)                          # additional options if required 


class SafeBrowsing(models.Model):

    enable              = models.BooleanField(default=False)
    bypass_to_localnet  = models.BooleanField(default=True)                    # connections to hosts in our LAN does not need to be filtered
    api_key             = models.CharField(max_length=200)                     # get it from google safe browsing API
    deny_url            = models.CharField(max_length=200)                     # for example, http://blocked.example.lan
    check_malware       = models.BooleanField(default=True) 
    check_social        = models.BooleanField(default=True) 
    check_unwanted_soft = models.BooleanField(default=False) 
    cache_clean         = models.IntegerField(default=60)                      # 0 seconds means no caching of clean results
    daemon_port         = models.IntegerField(default=18890)                   # default port on 127.0.0.1 that the wsgsbd daemon listens on for requests from URL rewriters
    
    helper_verbose      = models.BooleanField(default=False)
    helper_total        = models.IntegerField(default=20)
    helper_idle         = models.IntegerField(default=10)
    helper_startup      = models.IntegerField(default=5)