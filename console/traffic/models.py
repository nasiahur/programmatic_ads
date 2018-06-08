#
# system
#
import os
import json
import shutil

from _domain.core import Paths

#
# django
#
from django.db import models
from django.conf import settings

#
# 
#
class Traffic(models.Model):
    pass	

#
#
#
class WsMgrd(models.Model):

    WSMGRD_LOG_DEBUG   = 0
    WSMGRD_LOG_INFO    = 1
    WSMGRD_LOG_WARN    = 2
    WSMGRD_LOG_ERROR   = 3
    WSMGRD_LOG_CHOICES = ((WSMGRD_LOG_DEBUG, "debug"),(WSMGRD_LOG_INFO, "info"),(WSMGRD_LOG_WARN, "warning"),(WSMGRD_LOG_ERROR, "error"))

    logging    = models.IntegerField(choices=WSMGRD_LOG_CHOICES,default=WSMGRD_LOG_INFO)
    port       = models.IntegerField(default=18888)
    

#
# monitoring class
#
class Monitoring(models.Model):

    # global monitoring settings
    update_interval         = models.IntegerField(default=5)     # how often to write to .monitor files and process them
    history_normalize_names = models.BooleanField(default=True)  # if True user1@EXAMPLE.LAN gets normalized to user1 when uploading into history
    history_anonymize_names = models.BooleanField(default=False) # if True user name and user ip are set to '-' when uploading into history
    
    #
    # persistent channel settings
    #
    persistent_enable                          = models.BooleanField(default=True)
    persistent_purge                           = models.IntegerField(default=30)        # purge records older than N days
    persistent_store_query                     = models.BooleanField(default=False)
    persistent_store_path                      = models.BooleanField(default=False)
    persistent_store_clean                     = models.BooleanField(default=False)
    persistent_store_adblock                   = models.BooleanField(default=False)
    persistent_store_privacy                   = models.BooleanField(default=False)
    persistent_store_adult_heuristics          = models.BooleanField(default=True)
    persistent_store_adult_safesearch          = models.BooleanField(default=False)
    persistent_store_adult_youtube             = models.BooleanField(default=False)
    persistent_store_adult_phrases             = models.BooleanField(default=True)
    persistent_store_adult_image               = models.BooleanField(default=True)
    persistent_store_categories                = models.BooleanField(default=True)  # for categories, custom categories and dynamic categories
    persistent_store_http_sanitation           = models.BooleanField(default=True)
    persistent_store_content_content_type      = models.BooleanField(default=True)
    persistent_store_content_charset           = models.BooleanField(default=True)
    persistent_store_content_transfer_encoding = models.BooleanField(default=True)
    persistent_store_content_file_name         = models.BooleanField(default=True)
    persistent_store_content_file_type         = models.BooleanField(default=True)
    persistent_store_content_file_size         = models.BooleanField(default=True)
    persistent_store_apps                      = models.BooleanField(default=False)
    persistent_store_sslbump                   = models.BooleanField(default=False)

    #
    # realtime channel settings
    #
    realtime_enable                          = models.BooleanField(default=True)
    realtime_store_query                     = models.BooleanField(default=True)
    realtime_store_path                      = models.BooleanField(default=True)
    realtime_store_clean                     = models.BooleanField(default=True)
    realtime_store_adblock                   = models.BooleanField(default=True)
    realtime_store_privacy                   = models.BooleanField(default=True)
    realtime_store_adult_heuristics          = models.BooleanField(default=True)
    realtime_store_adult_safesearch          = models.BooleanField(default=True)
    realtime_store_adult_youtube             = models.BooleanField(default=True)
    realtime_store_adult_phrases             = models.BooleanField(default=True)
    realtime_store_adult_image               = models.BooleanField(default=True)
    realtime_store_categories                = models.BooleanField(default=True)    
    realtime_store_http_sanitation           = models.BooleanField(default=True)
    realtime_store_content_content_type      = models.BooleanField(default=True)
    realtime_store_content_charset           = models.BooleanField(default=True)
    realtime_store_content_transfer_encoding = models.BooleanField(default=True)
    realtime_store_content_file_name         = models.BooleanField(default=True)
    realtime_store_content_file_type         = models.BooleanField(default=True)
    realtime_store_content_file_size         = models.BooleanField(default=True)
    realtime_store_apps                      = models.BooleanField(default=True)
    realtime_store_sslbump                   = models.BooleanField(default=True)
    realtime_limit_record_count              = models.IntegerField(default=10000)

    #
    # access log channel
    #
    accesslog_enable                          = models.BooleanField(default=False)
    accesslog_store_query                     = models.BooleanField(default=False)
    accesslog_store_path                      = models.BooleanField(default=False)
    accesslog_store_clean                     = models.BooleanField(default=False)
    accesslog_store_adblock                   = models.BooleanField(default=False)
    accesslog_store_privacy                   = models.BooleanField(default=False)
    accesslog_store_adult_heuristics          = models.BooleanField(default=True)
    accesslog_store_adult_safesearch          = models.BooleanField(default=False)
    accesslog_store_adult_youtube             = models.BooleanField(default=False)
    accesslog_store_adult_phrases             = models.BooleanField(default=True)
    accesslog_store_adult_image               = models.BooleanField(default=True)
    accesslog_store_categories                = models.BooleanField(default=True)
    accesslog_store_http_sanitation           = models.BooleanField(default=True)
    accesslog_store_content_content_type      = models.BooleanField(default=True)
    accesslog_store_content_charset           = models.BooleanField(default=True)
    accesslog_store_content_transfer_encoding = models.BooleanField(default=True)
    accesslog_store_content_file_name         = models.BooleanField(default=True)
    accesslog_store_content_file_type         = models.BooleanField(default=True)
    accesslog_store_content_file_size         = models.BooleanField(default=True)
    accesslog_store_apps                      = models.BooleanField(default=False)
    accesslog_store_sslbump                   = models.BooleanField(default=False)

    #
    # syslog channel
    #
    syslog_enable                          = models.BooleanField(default=False)
    syslog_store_query                     = models.BooleanField(default=False)
    syslog_store_path                      = models.BooleanField(default=False)
    syslog_store_clean                     = models.BooleanField(default=False)
    syslog_store_adblock                   = models.BooleanField(default=False)
    syslog_store_privacy                   = models.BooleanField(default=False)
    syslog_store_adult_heuristics          = models.BooleanField(default=True)
    syslog_store_adult_safesearch          = models.BooleanField(default=False)
    syslog_store_adult_youtube             = models.BooleanField(default=False)
    syslog_store_adult_phrases             = models.BooleanField(default=True)
    syslog_store_adult_image               = models.BooleanField(default=True)
    syslog_store_categories                = models.BooleanField(default=True)
    syslog_store_http_sanitation           = models.BooleanField(default=True)
    syslog_store_content_content_type      = models.BooleanField(default=True)
    syslog_store_content_charset           = models.BooleanField(default=True)
    syslog_store_content_transfer_encoding = models.BooleanField(default=True)
    syslog_store_content_file_name         = models.BooleanField(default=True)
    syslog_store_content_file_type         = models.BooleanField(default=True)
    syslog_store_content_file_size         = models.BooleanField(default=True)
    syslog_store_apps                      = models.BooleanField(default=False)
    syslog_store_sslbump                   = models.BooleanField(default=False)


#
#
#
class SurfingNow(models.Model):

    COLUMN_NAME_NONE      = 0 # i.e. show all
    COLUMN_NAME_INCIDENT  = 1
    COLUMN_NAME_HOST      = 2
    COLUMN_NAME_USER      = 3
    COLUMN_NAME_IP        = 4
    COLUMN_NAME_POLICY    = 6
    COLUMN_NAME_MODULE    = 7
    COLUMN_NAME_VERDICT   = 8
    COLUMN_NAME_CHOICES = (
        (COLUMN_NAME_NONE,          "Show All"),
        (COLUMN_NAME_INCIDENT,      "Incident"),
        (COLUMN_NAME_HOST,          "Host"),
        (COLUMN_NAME_USER,          "User Name"),
        (COLUMN_NAME_IP,            "User IP"),
        (COLUMN_NAME_POLICY,        "Policy"),
        (COLUMN_NAME_MODULE,        "Module"),
        (COLUMN_NAME_VERDICT,       "Verdict"),
    )

    COLUMN_NAME_TO_DB_COLUMN = {
        COLUMN_NAME_NONE:           "",
        COLUMN_NAME_INCIDENT:       "iid",
        COLUMN_NAME_HOST:           "host",
        COLUMN_NAME_USER:           "user_name",
        COLUMN_NAME_IP:             "user_ip",
        COLUMN_NAME_POLICY:         "policy",
        COLUMN_NAME_MODULE:         "module",
        COLUMN_NAME_VERDICT:        "verdict",
    }

    column_name = models.IntegerField(default=COLUMN_NAME_NONE,choices=COLUMN_NAME_CHOICES)
    column_value  = models.CharField(max_length=254, default="")

#
#
#
class BrowsingHistory(models.Model):

    COLUMN_NAME_NONE      = 0 # i.e. show all
    COLUMN_NAME_INCIDENT  = 1
    COLUMN_NAME_HOST      = 2
    COLUMN_NAME_USER      = 3
    COLUMN_NAME_POLICY    = 6
    COLUMN_NAME_MODULE    = 7
    COLUMN_NAME_VERDICT   = 8
    COLUMN_NAME_CHOICES = (
        (COLUMN_NAME_NONE,          "Show All"),
        (COLUMN_NAME_INCIDENT,      "Incident"),
        (COLUMN_NAME_HOST,          "Host"),
        (COLUMN_NAME_USER,          "User Name"),
        (COLUMN_NAME_POLICY,        "Policy"),
        (COLUMN_NAME_MODULE,        "Module"),
        (COLUMN_NAME_VERDICT,       "Verdict"),
    )

    COLUMN_NAME_TO_DB_FILTER = {
        COLUMN_NAME_INCIDENT:       "iid",
        COLUMN_NAME_HOST:           "host__value__contains",
        COLUMN_NAME_USER:           "user_name__value__contains",
        COLUMN_NAME_POLICY:         "policy__value__contains",
        COLUMN_NAME_MODULE:         "module__value__contains",
        COLUMN_NAME_VERDICT:        "verdict__value__contains",
    }

    column_name  = models.IntegerField(default=COLUMN_NAME_NONE,choices=COLUMN_NAME_CHOICES)
    column_value = models.CharField(max_length=254, default="")


#
# reporter
#
class Reporter(models.Model):

    # smtp connection settings
    smtp_username = models.CharField(max_length=254, blank=True)
    smtp_password = models.CharField(max_length=254, blank=True)
    smtp_server   = models.CharField(max_length=254, blank=True)
    smtp_port     = models.IntegerField(default=587)
    smtp_use_auth = models.BooleanField(default=True)

#
# parameters
#
PARAMETER_TIMEFRAME_LASTNDAYS   = 'last_n_days'
PARAMETER_TIMEFRAME_LASTNWEEKS  = 'last_n_weeks'
PARAMETER_TIMEFRAME_LASTNMONTHS = 'last_n_months'
PARAMETER_TIMEFRAME_FROMTO      = 'from_to'

PARAMETER_TIMEFRAME_CHOICES = (
    (PARAMETER_TIMEFRAME_LASTNDAYS, 'Last N days'),
    (PARAMETER_TIMEFRAME_LASTNWEEKS, 'Last N weeks'),
    (PARAMETER_TIMEFRAME_LASTNMONTHS, 'Last N months'),
    (PARAMETER_TIMEFRAME_FROMTO, 'Specific date interval'),
)

#
# jobs
#
REPORT_JOB_RUNONCE  = 'manual'
REPORT_JOB_PERIODIC = 'automatic'

REPORT_JOB_CHOICES = (
    (REPORT_JOB_RUNONCE, 'Manually'),
    (REPORT_JOB_PERIODIC, 'Automatically (Periodic)'),
)

#
# task that builds a report out of template
#
class Job(models.Model):

    name      = models.CharField(max_length=254, unique=True)    # name of report job, must be unique
    enabled   = models.BooleanField(default=True)   # if disable report job is not active *but* still visible in Web UI
    email     = models.TextField()                  # list of addresses separated by comma to e-mail report to after generation
    comments  = models.TextField()                  # need for the admin only

    # schedule cron style
    # schedule_type   = models.CharField(max_length=64, choices=REPORT_JOB_CHOICES, default=REPORT_JOB_PERIODIC)
    schedule_min    = models.CharField(max_length=64, default='*')
    schedule_hour   = models.CharField(max_length=64, default='*')
    schedule_dom    = models.CharField(max_length=64, default='*')
    schedule_month  = models.CharField(max_length=64, default='*')
    schedule_dow    = models.CharField(max_length=64, default='*')

    # report template values
    template_type   = models.CharField(max_length=255, default='*')

    # time frame specs for result set
    timeframe_type  = models.CharField(max_length=64, choices=PARAMETER_TIMEFRAME_CHOICES, default=PARAMETER_TIMEFRAME_LASTNDAYS)
    timeframe_value = models.IntegerField(default=30)
    timeframe_from  = models.DateField(null=True, blank=True)
    timeframe_to    = models.DateField(null=True, blank=True)

    # inclusions
    include_domains    = models.TextField()	  # items separated by comma
    include_users      = models.TextField()   # items separated by comma
    include_policies   = models.TextField()   # items separated by comma
    include_categories = models.TextField()   # items separated by comma

    # exclusions
    exclude_domains    = models.TextField()	  # items separated by comma
    exclude_users      = models.TextField()   # items separated by comma
    exclude_policies   = models.TextField()   # items separated by comma
    exclude_categories = models.TextField()   # items separated by comma

    # other settings
    include_current   = models.BooleanField(default=True)
    limit_n_entries   = models.IntegerField(default=50)
    limit_n_drilldown = models.IntegerField(default=50)		# not more than n records is shown in drill down

    def __unicode__(self):
        return self.name

    def schedule_str(self):
        text = ""
        try:
            if self.schedule_type == REPORT_JOB_RUNONCE:
                text = "Manual"
            else:
                text = "Periodic"
        except Exception as e:
            text = str(e)

        return text

    def params_str(self):
        text = ""
        try:
            if self.timeframe_type == PARAMETER_TIMEFRAME_FROMTO:
                text = "From %s to %s" % (self.timeframe_from, self.timeframe_to)
            else:
                text = "Last %d" % self.timeframe_value
                if self.timeframe_type == PARAMETER_TIMEFRAME_LASTNDAYS:
                    text += " days"
                elif self.timeframe_type == PARAMETER_TIMEFRAME_LASTNWEEKS:
                    text += " weeks"
                elif self.timeframe_type == PARAMETER_TIMEFRAME_LASTNMONTHS:
                    text += " months"
                else:
                    text += " items"


        except Exception as e:
            text = str(e)

        return text

    def get_meta(self):

        meta = {}

        try:
            path = os.path.join(Paths.var_dir(), "reports", self.name, "data", "meta.json")
            if os.path.isfile(path):
                with open(path) as fin:
                    meta = json.load(fin)
        except Exception as e:
            pass

        return meta

    def logfile_exists(self):

        path = os.path.join(Paths.var_dir(), "reports", self.name, "data", "report.log")
        if os.path.isfile(path):
            return True

        return False

    def generated_finished(self):

        try:
            path = os.path.join(Paths.var_dir(), "reports", self.name, "data", "progress")
            if os.path.isfile(path):
                with open(path, 'r') as fin:
                    data = fin.read().replace('\n', '')
                    if int(data) == 100:
                        return True
        except Exception as e:
            pass

        return False

    def generated_on(self):

        meta = self.get_meta()
        if 'builtOnLocal' in meta:
            return meta['builtOnLocal']
        if 'builtOn' in meta:
            return meta['builtOn']
        return "not yet generated"

    def remove_generated_dir(self):
        try:
            path = os.path.join(Paths.var_dir(), "reports", self.name)
            if os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            pass

    def records_from(self):

        meta = self.get_meta()
        if 'start' in meta:
            return meta['start']

        return "<ERROR>"

    def records_to(self):

        meta = self.get_meta()
        if 'end' in meta:
            return meta['end']

        return "<ERROR>"


#
# type of ICAP message (OPTIONS, REQMOD, RESPMOD)
#
class Message(models.Model):

    class Meta:
        db_table = 'monitor_message'

    value = models.CharField(db_index=True, max_length=16, unique=True)

    def __unicode__(self):
        return "Message - %d:%s" % (self.pk, self.value)

#
# IP address of the proxy client (and host name if resolved)
#
class UserIP(models.Model):

    class Meta:
        db_table = 'monitor_userip'

    value = models.CharField(db_index=True, max_length=64, unique=True)
    #host  = models.CharField(max_length=254)

    def __unicode__(self):
        return "User IP - %d:%s" % (self.pk, self.value)

#
# name of the proxy client (if squid supports authentication)
#
class UserName(models.Model):

    class Meta:
        db_table = 'monitor_username'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "User Name - %d:%s" % (self.pk, self.value)

#
#
#
class UserAgent(models.Model):

    class Meta:
        db_table = 'monitor_useragent'

    value = models.TextField()

    def __unicode__(self):
        return "User Agent - %d:%s" % (self.pk, self.value)

#
#
#
class UserEui(models.Model):

    class Meta:
        db_table = 'monitor_usereui'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "User EUI - %d:%s" % (self.pk, self.value)



#
# name of the policy
#
class Policy(models.Model):

    class Meta:
        db_table = 'monitor_policy'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "Policy - %d:%s" % (self.pk, self.value)

#
# name of policy member that triggered policy matching
#
class Member(models.Model):

    class Meta:
        db_table = 'monitor_member'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "Member - %d:%s" % (self.pk, self.value)

#
#
#
class Method(models.Model):

    class Meta:
        db_table = 'monitor_method'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "Method - %d:%s" % (self.pk, self.value)

#
#
#
class Scheme(models.Model):

    class Meta:
        db_table = 'monitor_scheme'

    value = models.CharField(db_index=True, max_length=16, unique=True)

    def __unicode__(self):
        return "Scheme - %d:%s" % (self.pk, self.value)

#
#
#
class Host(models.Model):

    class Meta:
        db_table = 'monitor_host'

    value = models.CharField(db_index=True, max_length=254, unique=True)

    category1 = models.IntegerField()
    category2 = models.IntegerField()
    category3 = models.IntegerField()
    category4 = models.IntegerField()
    category5 = models.IntegerField()
    category6 = models.IntegerField()
    category7 = models.IntegerField()
    category8 = models.IntegerField()

    def __unicode__(self):
        return "Host - %d:%s" % (self.pk, self.value)

#
#
#
class Tld(models.Model):

    class Meta:
        db_table = 'monitor_tld'

    value = models.CharField(db_index=True, max_length=254, unique=True)

    def __unicode__(self):
        return "Top Level Domain - %d:%s" % (self.pk, self.value)


#
#
#
class Path(models.Model):

    class Meta:
        db_table = 'monitor_path'

    value = models.CharField(db_index=True, max_length=254, unique=True)
    def __unicode__(self):
        return "Path - %d:%s" % (self.pk, self.value)

#
#
#
class Query(models.Model):

    class Meta:
        db_table = 'monitor_query'

    value = models.TextField()
    def __unicode__(self):
        return "Query - %d:%s" % (self.pk, self.value)

#
#
#
class Verdict(models.Model):

    class Meta:
        db_table = 'monitor_verdict'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "Verdict - %d:%s" % (self.pk, self.value)

#
#
#
class Level(models.Model):

    class Meta:
        db_table = 'monitor_level'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "Level - %d:%s" % (self.pk, self.value)

#
#
#
class Module(models.Model):

    class Meta:
        db_table = 'monitor_module'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "Module - %d:%s" % (self.pk, self.value)

#
#
#
class Server(models.Model):

    class Meta:
        db_table = 'monitor_server'

    value = models.CharField(db_index=True, max_length=254, unique=True)

    def __unicode__(self):
        return "Server - %d:%s" % (self.pk, self.value)

#
#
#
class ScanFlags(models.Model):

    class Meta:
        db_table = 'monitor_scanflags'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "ScanFlags - %d:%s" % (self.pk, self.value)

#
#
#
class Categories(models.Model):

    class Meta:
        db_table = 'monitor_categories'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "Categories - %d:%s" % (self.pk, self.value)

    def int2string(self, value_int):
        try:
            return Categories.objects.get(pk=value_int).value
        except Exception as e:
            return "N/A"

#
#
#
class ContentType(models.Model):

    class Meta:
        db_table = 'monitor_contenttype'

    value = models.CharField(db_index=True, max_length=64, unique=True)

    def __unicode__(self):
        return "ContentType - %d:%s" % (self.pk, self.value)

#
#
#
class Param1(models.Model):

    class Meta:
        db_table = 'monitor_param1'

    value = models.CharField(db_index=True, max_length=64, unique=True)
    def __unicode__(self):
        return "Param1 - %d:%s" % (self.pk, self.value)

#
#
#
class Param2(models.Model):

    class Meta:
        db_table = 'monitor_param2'

    value = models.CharField(db_index=True, max_length=254, unique=True)
    def __unicode__(self):
        return "Param2 - %d:%s" % (self.pk, self.value)


#
#
#
class Event(models.Model):

    class Meta:
        db_table = 'monitor_event'

    iid          = models.IntegerField(db_index=True, default=0)    # incident id (uniquely identifies each message)
    timestamp    = models.DateTimeField()                           # timestamp in UTC
    date         = models.DateField(db_index=True)                  # date parsed out from timestamp
    time         = models.TimeField(db_index=True)                  # time parsed out from timestamp
    hour         = models.IntegerField(db_index=True, default=0)    # hour of day [0-23]
    server       = models.ForeignKey(Server)
    message      = models.ForeignKey(Message)
    user_name    = models.ForeignKey(UserName)
    user_ip      = models.ForeignKey(UserIP)
    user_agent   = models.ForeignKey(UserAgent)
    user_eui     = models.ForeignKey(UserEui)    
    size         = models.IntegerField(db_index=True, default=0)    # size of the request/response in bytes
    size_approx  = models.IntegerField(db_index=True, default=0)    # size of the request/response in bytes taken from Content-Length field
    #duration     = models.IntegerField(db_index=True, default=0)    # processing Time (in milliseconds) spent within module
    #timing       = models.IntegerField(db_index=True, default=0)    # processing Time (in milliseconds) spent within processor
    #flags        = models.ManyToManyField(ScanFlags)                # exclusion flags
    scanflags    = models.IntegerField(db_index=True, default=0)     # exclusion flags
    trusted      = models.IntegerField(db_index=True, default=0)
    policy       = models.ForeignKey(Policy)
    member       = models.ForeignKey(Member)
    content_type = models.ForeignKey(ContentType)
    level        = models.ForeignKey(Level)
    verdict      = models.ForeignKey(Verdict)
    offensive    = models.BooleanField(db_index=True, default=False)# True if offensive (verdict is blocked; module is not adblock or privacy)
    unproductive = models.BooleanField(db_index=True, default=False)# True if non productive
    method       = models.ForeignKey(Method)
    module       = models.ForeignKey(Module)
    param1       = models.ForeignKey(Param1)
    param2       = models.ForeignKey(Param2)
    #mtime        = models.IntegerField(db_index=True, default=0)    # module scan time
    scheme       = models.ForeignKey(Scheme)
    host         = models.ForeignKey(Host)                          # host
    tld          = models.ForeignKey(Tld)                           # top level domain (parent of host)
    path         = models.ForeignKey(Path)                          # /path/to/index
    query        = models.ForeignKey(Query)                         # URL part after ?

    ref_scheme   = models.ForeignKey(Scheme, related_name="ref_scheme_id")
    ref_host     = models.ForeignKey(Host, related_name="ref_host_id")
    #ref_path     = models.ForeignKey(Path, related_name="ref_path_id")

    def __unicode__(self):
        return "%d|%s" % (self.iid, self.host)

    def get_url(self):
        result = ""
        if len(self.scheme.value) > 0:
            result = self.scheme.value + "://"

        result = result + self.host.value
        result = result + self.path.value
        return result

    def get_referer(self):
        result = ""
        if len(self.ref_scheme.value) > 0:
            result = self.ref_scheme.value + "://"

        result = result + self.ref_host.value
        #result = result + self.ref_path.value
        return result

    def is_whitelisted(self):
        if self.scanflags == 0:
            return True
        return False


    def parse_flags(self, flags):

        # these are bits for flags
        scan_for_adult             = 1
        scan_for_categories        = 1<<1
        scan_for_categories_custom = 1<<2
        scan_for_file              = 1<<3
        scan_for_adblock           = 1<<4
        scan_for_privacy           = 1<<5
        scan_for_http              = 1<<6

        result = { 'adult': False, 'categories': False, 'custom': False, 'file': False, 'adblock': False, 'privacy': False, 'http': False }
        if flags & scan_for_adult:
            result['adult'] = True
        if flags & scan_for_categories:
            result['categories'] = True
        if flags & scan_for_categories_custom:
            result['custom'] = True
        if flags & scan_for_file:
            result['file'] = True
        if flags & scan_for_adblock:
            result['adblock'] = True
        if flags & scan_for_privacy:
            result['privacy'] = True
        if flags & scan_for_http:
            result['http'] = True

        return result

    def get_flags_as_string(self):

        array = []
        result = self.parse_flags(self.scanflags)
        for key, value in result.iteritems():
            if value is True:
                array.append(key)
        return ", ".join(array)

    def get_categories_as_string(self):
        array = []

        if self.host.category1 != None and self.host.category1 != 0:
            array.append(self.host.category1)
        if self.host.category2 != None and self.host.category2 != 0:
            array.append(self.host.category2)
        if self.host.category3 != None and self.host.category3 != 0:
            array.append(self.host.category3)
        if self.host.category4 != None and self.host.category4 != 0:
            array.append(self.host.category4)
        if self.host.category5 != None and self.host.category5 != 0:
            array.append(self.host.category5)
        if self.host.category6 != None and self.host.category6 != 0:
            array.append(self.host.category6)
        if self.host.category7 != None and self.host.category7 != 0:
            array.append(self.host.category7)
        if self.host.category8 != None and self.host.category8 != 0:
            array.append(self.host.category8)

        values = []
        for a in array:
            values.append(Categories().int2string(a))

        return ", ".join(values)
