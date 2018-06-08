import os
import shutil

#
# domain
#
from _domain.utils import FileWriter, JsonDumper

#
# ours
#
from utility.generator import BaseGenerator
from traffic.models import *
from squid.models import Network
from console.settings import DATABASES

#
#
#
class Generator(BaseGenerator):

    #
    #
    #
    def __init__(self, root_dir):

        # call the base class
        super(Generator, self).__init__(root_dir)

    def generate_config(self, target_dir):

        # create writer and dumper
        w = FileWriter(target_dir)
        d = JsonDumper()

        # and generate
        self.generate_reports(w, d)
        self.generate_monitor(w, d)
        self.generate_wsmgrd(w, d)

    #
    #
    #
    def generate_reports(self, writer, dumper):

        # save reporter
        reporter = Reporter.objects.first()
        data     = {
            'smtp_user' : {
                'smtp_server'             : reporter.smtp_server,
                'port'                    : reporter.smtp_port,
                'username'                : reporter.smtp_username,
                'password'                : reporter.smtp_password,
                'authentication_required' : reporter.smtp_use_auth,
            },
            'jobs' : [],
            'disabled_jobs': [] # this is actually needed for application upgrade only!
        }

        # save all jobs
        for item in Job.objects.all():
            
            section = None
            if item.enabled:
                section = "jobs"
            else:
                section = "disabled_jobs"

            data[section].append(self.generate_job(item))

        # and write file
        writer.write('reports.json', dumper.dumps(data))

    #
    #
    #
    def generate_job(self, job):

        data = {
            'name'     : job.name,
            'comments' : job.comments,
            'email'    : job.email,
            'template' : job.template_type,
            'schedule' : {
                'type'  : "automatic",
                'min'   : job.schedule_min,
                'hour'  : job.schedule_hour,
                'dom'   : job.schedule_dom,
                'month' : job.schedule_month,
                'dow'   : job.schedule_dow,
            },
            'params' : {
                'timeframe_type'  : job.timeframe_type,
                'timeframe_value' : job.timeframe_value,
                'timeframe_from'  : self.to_isoformat(job.timeframe_from),
                'timeframe_to'    : self.to_isoformat(job.timeframe_to),
                'include_current' : job.include_current,
                'limit_n_entries' : job.limit_n_entries,
                'limit_n_drilldown' : job.limit_n_drilldown,
            },
            'limits' : {
                'include_domains'    : self.generate_list(job.include_domains),
                'include_users'      : self.generate_list(job.include_users),
                'include_policies'   : self.generate_list(job.include_policies),
                'include_categories' : self.generate_list(job.include_categories),

                'exclude_domains'    : self.generate_list(job.exclude_domains),
                'exclude_users'      : self.generate_list(job.exclude_users),
                'exclude_policies'   : self.generate_list(job.exclude_policies),
                'exclude_categories' : self.generate_list(job.exclude_categories),
            }
        }
        return data

    def generate_list(self, value_str):

        array = []
        for item in value_str.split(","):
            item = item.strip()
            if len(item) == 0:
                continue

            if item not in array:
                array.append(item)
        return array

    def to_isoformat(self, date):
        if not date:
            return None
        else:
            return date.isoformat()


    #
    #
    #
    def generate_wsmgrd(self, writer, dumper):

        wsmgrd  = WsMgrd.objects.first()
        network = Network.objects.first()
        d = { 
            "rest_service" : {
                "port"      : wsmgrd.port,
                "squid_port": network.explicit_port
            },
            "logging" : wsmgrd.logging,
        }
        writer.write('wsmgrd.json', dumper.dumps(d))

    #
    #
    #
    def generate_monitor(self, writer, dumper):

        monitor = Monitoring.objects.first()

        # init defaults
        d = {
            'update_interval' : monitor.update_interval,
            'history_normalize_names' : monitor.history_normalize_names,
            'history_anonymize_names' : monitor.history_anonymize_names,
            'persistent' : {
                'enable' : monitor.persistent_enable,
                'purge'  : monitor.persistent_purge,
                "purge_schedule": {
                    "dom": "*",
                    "dow": "*",
                    "hour": "1",
                    "min": "4",
                    "month": "*"
                }, 
                'active'  : 'sqlite3',
                "sqlite3" : { "dummy" : 0 },
                "mysql" : { 
                    "name" : "websafety_monitor",
                    "user" : "root",
                    "password" : "Passw0rd",
                    "host" : "127.0.0.1",
                    "port" : 3306,
                    "params": "autocommit=0&innodb_support_xa=0&parseTime=true&tx_isolation=%27READ-COMMITTED%27", 
                    "protocol": "tcp"
                },
                'store_query': monitor.persistent_store_query,
                'store_path': monitor.persistent_store_path,
                'store_clean' : monitor.persistent_store_clean,
                'store_adblock' : monitor.persistent_store_adblock,
                'store_privacy' : monitor.persistent_store_privacy,
                'store_adult_heuristics' : monitor.persistent_store_adult_heuristics,
                'store_adult_safesearch' : monitor.persistent_store_adult_safesearch,
                'store_adult_youtube' : monitor.persistent_store_adult_youtube,
                'store_adult_phrases' : monitor.persistent_store_adult_phrases,
                'store_adult_image' : monitor.persistent_store_adult_image,
                'store_categories' : monitor.persistent_store_categories,
                'store_http_sanitation' : monitor.persistent_store_http_sanitation,
                'store_content_content_type' : monitor.persistent_store_content_content_type,
                'store_content_charset' : monitor.persistent_store_content_charset,
                'store_content_transfer_encoding' : monitor.persistent_store_content_transfer_encoding,
                'store_content_file_name' : monitor.persistent_store_content_file_name,
                'store_content_file_type' : monitor.persistent_store_content_file_type,
                'store_content_file_size' : monitor.persistent_store_content_file_size,
                'store_apps' : monitor.persistent_store_apps,
                'store_sslbump' : monitor.persistent_store_sslbump
            },
            'realtime' : {
                'enable' : monitor.realtime_enable,
                'limit_record_count' : monitor.realtime_limit_record_count,
                'store_query': monitor.realtime_store_query,
                'store_path': monitor.realtime_store_path,
                'store_clean' : monitor.realtime_store_clean,
                'store_adblock' : monitor.realtime_store_adblock,
                'store_privacy' : monitor.realtime_store_privacy,
                'store_adult_heuristics' : monitor.realtime_store_adult_heuristics,
                'store_adult_safesearch' : monitor.realtime_store_adult_safesearch,
                'store_adult_youtube' : monitor.realtime_store_adult_youtube,
                'store_adult_phrases' : monitor.realtime_store_adult_phrases,
                'store_adult_image' : monitor.realtime_store_adult_image,
                'store_categories' : monitor.realtime_store_categories,
                'store_http_sanitation' : monitor.realtime_store_http_sanitation,
                'store_content_content_type' : monitor.realtime_store_content_content_type,
                'store_content_charset' : monitor.realtime_store_content_charset,
                'store_content_transfer_encoding' : monitor.realtime_store_content_transfer_encoding,
                'store_content_file_name' : monitor.realtime_store_content_file_name,
                'store_content_file_type' : monitor.realtime_store_content_file_type,
                'store_content_file_size' : monitor.realtime_store_content_file_size,
                'store_apps' : monitor.realtime_store_apps,
                'store_sslbump' : monitor.realtime_store_sslbump
            },
            'syslog' : {
                'enable' : monitor.syslog_enable,
                'store_query': monitor.syslog_store_query,
                'store_path': monitor.syslog_store_path,
                'store_clean' : monitor.syslog_store_clean,
                'store_adblock' : monitor.syslog_store_adblock,
                'store_privacy' : monitor.syslog_store_privacy,
                'store_adult_heuristics' : monitor.syslog_store_adult_heuristics,
                'store_adult_safesearch' : monitor.syslog_store_adult_safesearch,
                'store_adult_youtube' : monitor.syslog_store_adult_youtube,
                'store_adult_phrases' : monitor.syslog_store_adult_phrases,
                'store_adult_image' : monitor.syslog_store_adult_image,
                'store_categories' : monitor.syslog_store_categories,
                'store_http_sanitation' : monitor.syslog_store_http_sanitation,
                'store_content_content_type' : monitor.syslog_store_content_content_type,
                'store_content_charset' : monitor.syslog_store_content_charset,
                'store_content_transfer_encoding' : monitor.syslog_store_content_transfer_encoding,
                'store_content_file_name' : monitor.syslog_store_content_file_name,
                'store_content_file_type' : monitor.syslog_store_content_file_type,
                'store_content_file_size' : monitor.syslog_store_content_file_size,
                'store_apps' : monitor.syslog_store_apps,
                'store_sslbump' : monitor.syslog_store_sslbump,
            }, 
            'accesslog' : {
                'enable' : monitor.accesslog_enable,
                'store_query': monitor.accesslog_store_query,
                'store_path': monitor.accesslog_store_path,
                'store_clean' : monitor.accesslog_store_clean,
                'store_adblock' : monitor.accesslog_store_adblock,
                'store_privacy' : monitor.accesslog_store_privacy,
                'store_adult_heuristics' : monitor.accesslog_store_adult_heuristics,
                'store_adult_safesearch' : monitor.accesslog_store_adult_safesearch,
                'store_adult_youtube' : monitor.accesslog_store_adult_youtube,
                'store_adult_phrases' : monitor.accesslog_store_adult_phrases,
                'store_adult_image' : monitor.accesslog_store_adult_image,
                'store_categories' : monitor.accesslog_store_categories,
                'store_http_sanitation' : monitor.accesslog_store_http_sanitation,
                'store_content_content_type' : monitor.accesslog_store_content_content_type,
                'store_content_charset' : monitor.accesslog_store_content_charset,
                'store_content_transfer_encoding' : monitor.accesslog_store_content_transfer_encoding,
                'store_content_file_name' : monitor.accesslog_store_content_file_name,
                'store_content_file_type' : monitor.accesslog_store_content_file_type,
                'store_content_file_size' : monitor.accesslog_store_content_file_size,
                'store_apps' : monitor.accesslog_store_apps,
                'store_sslbump' : monitor.accesslog_store_sslbump,
            }
        }

        # now adjust defaults based on database selected
        is_sqlite = (DATABASES['monitor']['ENGINE'] == 'django.db.backends.sqlite3')
        if is_sqlite:
            d['persistent']['active']            = 'sqlite3'
        else:
            d['persistent']['active']            = 'mysql'
            d['persistent']['mysql']['name']     = DATABASES['monitor']['NAME']
            d['persistent']['mysql']['user']     = DATABASES['monitor']['USER']
            d['persistent']['mysql']['password'] = DATABASES['monitor']['PASSWORD']
            d['persistent']['mysql']['host']     = DATABASES['monitor']['HOST']
            d['persistent']['mysql']['port']     = int(DATABASES['monitor']['PORT'])

        writer.write('monitor.json', dumper.dumps(d))
