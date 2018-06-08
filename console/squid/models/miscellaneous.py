from django.db import models

#
#
#
class Miscellaneous(models.Model):

    #NOT_MANAGED: configuration_includes_quoted_values
    #NOT_MANAGED: memory_pools
    #NOT_MANAGED: memory_pools_limit
    #NOT_MANAGED: cachemgr_passwd
    #NOT_MANAGED: client_db
    #NOT_MANAGED: refresh_all_ims
    #NOT_MANAGED: reload_into_ims
    #NOT_MANAGED: connect_retries
    #NOT_MANAGED: retry_on_error
    #NOT_MANAGED: as_whois_server
    #NOT_MANAGED: offline_mode
    #NOT_MANAGED: uri_whitespace
    #NOT_MANAGED: chroot
    #NOT_MANAGED: balance_on_multiple_ip
    #NOT_MANAGED: pipeline_prefetch
    #NOT_MANAGED: high_response_time_warning
    #NOT_MANAGED: high_page_fault_warning
    #NOT_MANAGED: high_memory_warning
    #NOT_MANAGED: sleep_after_fork
    #NOT_MANAGED: windows_ipaddrchangemonitor
    #NOT_MANAGED: eui_lookup
    #NOT_MANAGED: max_filedescriptors

    # forwarded_for configuration
    FORWARDED_FOR_OFF         = 0
    FORWARDED_FOR_ON          = 1
    FORWARDED_FOR_TRANSPARENT = 2
    FORWARDED_FOR_TRUNCATE    = 3
    FORWARDED_FOR_DELETE      = 4
    FORWARDED_FOR_CHOICES     = (
        (FORWARDED_FOR_OFF,         "off"), 
        (FORWARDED_FOR_ON,          "on (default)"), 
        (FORWARDED_FOR_TRANSPARENT, "transparent"),
        (FORWARDED_FOR_TRUNCATE,    "truncate"),
        (FORWARDED_FOR_DELETE,      "delete"),
    )

    forwarded_for = models.IntegerField(choices=FORWARDED_FOR_CHOICES,default=FORWARDED_FOR_ON)