import os

#
#
#
from _domain.utils import read_json_object

#
#
#
from traffic.models import Monitoring, Reporter, Job

#
#
#
class Upgrader(object):

    def __init__(self, major, minor):

        self.major   = major
        self.minor   = minor

    def upgrade(self, etc_dir):

        self.upgrade_monitor(etc_dir)
        self.upgrade_reports(etc_dir)


    def upgrade_reports(self, etc_dir):

        path = os.path.join(etc_dir, "traffic", "reports.json")
        if not os.path.exists(path):
            return

        if self.major < 5:
            return
        if self.major == 5 and self.minor < 2:
            return

        # get json and upgrade
        data = read_json_object(path)

        # upgrade smtp settings
        if True:

            obj  = Reporter.objects.first()
            obj.smtp_use_auth = data['smtp_user']['authentication_required']
            obj.smtp_username = data['smtp_user']['username']
            obj.smtp_password = data['smtp_user']['password']
            obj.smtp_server   = data['smtp_user']['smtp_server']
            obj.smtp_port     = data['smtp_user']['port']
            obj.save()

        # upgrade jobs
        if True:

            for job in data['jobs']:

                obj, created = Job.objects.get_or_create(name=job['name'])

                obj.email         = job['email']
                obj.comments      = job['comments']
                obj.template_type = job['template']
                obj.enabled       = True
                obj.include_current   = job['params']['include_current']
                obj.limit_n_drilldown = job['params']['limit_n_drilldown']
                obj.limit_n_entries   = job['params']['limit_n_entries']

                obj.timeframe_from  = job['params']['timeframe_from']
                obj.timeframe_to    = job['params']['timeframe_to']
                obj.timeframe_type  = job['params']['timeframe_type']
                obj.timeframe_value = job['params']['timeframe_value']

                obj.schedule_min   = job['schedule']['min']
                obj.schedule_hour  = job['schedule']['hour']
                obj.schedule_dom   = job['schedule']['dom']
                obj.schedule_month = job['schedule']['month']
                obj.schedule_dow   = job['schedule']['dow']

                # items separated by comma
                obj.include_domains    = ",".join(job['limits']['include_domains'])
                obj.include_users      = ",".join(job['limits']['include_users'])
                obj.include_policies   = ",".join(job['limits']['include_policies'])
                obj.include_categories = ",".join(job['limits']['include_categories'])
                obj.exclude_domains    = ",".join(job['limits']['exclude_domains'])
                obj.exclude_users      = ",".join(job['limits']['exclude_users'])
                obj.exclude_policies   = ",".join(job['limits']['exclude_policies'])
                obj.exclude_categories = ",".join(job['limits']['exclude_categories'])

                obj.save()

        
    def upgrade_monitor(self, etc_dir):

        # first try newer path
        path = os.path.join(etc_dir, "traffic", "monitor.json")
        if not os.path.exists(path):
            path = os.path.join(etc_dir, "monitor.json")

        # get json and upgrade
        data = read_json_object(path)
        obj  = Monitoring.objects.first()

        if 'database' in data:

            src                                            = data['database']
            obj.persistent_enable                          = src['enable']
            obj.persistent_purge                           = src['purge']
            obj.persistent_store_clean                     = src['store_clean']
            obj.persistent_store_adblock                   = src['store_adblock']
            obj.persistent_store_privacy                   = src['store_privacy']
            obj.persistent_store_adult_heuristics          = src['store_adult_heuristics']
            obj.persistent_store_adult_safesearch          = src['store_adult_safesearch']
            obj.persistent_store_adult_youtube             = src['store_adult_youtube']
            obj.persistent_store_adult_phrases             = src['store_adult_phrases']
            obj.persistent_store_adult_image               = src['store_adult_image']

            # some custom logic for categories
            if True:

                # set default value to true
                obj.persistent_store_categories = True

                # see if we need to reset it to false
                cat1 = src.get('store_categories', False)
                cat2 = src.get('store_categories_dynamic', False)
                cat3 = src.get('store_custom', False)

                if not (cat1 or cat2 or cat3):
                    obj.persistent_store_categories = False

            obj.persistent_store_http_sanitation           = src['store_http_sanitation']
            obj.persistent_store_content_content_type      = src['store_content_content_type']
            obj.persistent_store_content_charset           = src['store_content_charset']
            obj.persistent_store_content_transfer_encoding = src['store_content_transfer_encoding']
            obj.persistent_store_content_file_name         = src['store_content_file_name']
            obj.persistent_store_content_file_type         = src['store_content_file_type']
            obj.persistent_store_content_file_size         = src['store_content_file_size']
            obj.persistent_store_apps                      = src['store_apps']
            obj.persistent_store_sslbump                   = src['store_sslbump']
            
        if 'logfile' in data:

            src                                            = data['logfile']
            obj.accesslog_enable                           = src['enable']
            obj.accesslog_store_clean                      = src['store_clean']
            obj.accesslog_store_adblock                    = src['store_adblock']
            obj.accesslog_store_privacy                    = src['store_privacy']
            obj.accesslog_store_adult_heuristics           = src['store_adult_heuristics']
            obj.accesslog_store_adult_safesearch           = src['store_adult_safesearch']
            obj.accesslog_store_adult_youtube              = src['store_adult_youtube']
            obj.accesslog_store_adult_phrases              = src['store_adult_phrases']
            obj.accesslog_store_adult_image                = src['store_adult_image']

            # some custom logic for categories
            if True:

                # set default value to true
                obj.accesslog_store_categories = True

                # see if we need to reset it to false
                cat1 = src.get('store_categories', False)
                cat2 = src.get('store_categories_dynamic', False)
                cat3 = src.get('store_custom', False)

                if not (cat1 or cat2 or cat3):
                    obj.accesslog_store_categories = False

            obj.accesslog_store_http_sanitation            = src['store_http_sanitation']
            obj.accesslog_store_content_content_type       = src['store_content_content_type']
            obj.accesslog_store_content_charset            = src['store_content_charset']
            obj.accesslog_store_content_transfer_encoding  = src['store_content_transfer_encoding']
            obj.accesslog_store_content_file_name          = src['store_content_file_name']
            obj.accesslog_store_content_file_type          = src['store_content_file_type']
            obj.accesslog_store_content_file_size          = src['store_content_file_size']
            obj.accesslog_store_apps                       = src['store_apps']
            obj.accesslog_store_sslbump                    = src['store_sslbump']

        if 'memory' in data:

            src                                            = data['memory']
            obj.realtime_enable                            = src['enable']
            obj.realtime_store_clean                       = src['store_clean']
            obj.realtime_store_adblock                     = src['store_adblock']
            obj.realtime_store_privacy                     = src['store_privacy']
            obj.realtime_store_adult_heuristics            = src['store_adult_heuristics']
            obj.realtime_store_adult_safesearch            = src['store_adult_safesearch']
            obj.realtime_store_adult_youtube               = src['store_adult_youtube']
            obj.realtime_store_adult_phrases               = src['store_adult_phrases']
            obj.realtime_store_adult_image                 = src['store_adult_image']

            # some custom logic for categories
            if True:

                # set default value to true
                obj.realtime_store_categories = True

                # see if we need to reset it to false
                cat1 = src.get('store_categories', False)
                cat2 = src.get('store_categories_dynamic', False)
                cat3 = src.get('store_custom', False)

                if not (cat1 or cat2 or cat3):
                    obj.realtime_store_categories = False

            obj.realtime_store_http_sanitation             = src['store_http_sanitation']
            obj.realtime_store_content_content_type        = src['store_content_content_type']
            obj.realtime_store_content_charset             = src['store_content_charset']
            obj.realtime_store_content_transfer_encoding   = src['store_content_transfer_encoding']
            obj.realtime_store_content_file_name           = src['store_content_file_name']
            obj.realtime_store_content_file_type           = src['store_content_file_type']
            obj.realtime_store_content_file_size           = src['store_content_file_size']
            obj.realtime_store_apps                        = src['store_apps']
            obj.realtime_store_sslbump                     = src['store_sslbump']

        if 'syslog' in data:

            src                                            = data['syslog']
            obj.syslog_enable                              = src['enable']
            obj.syslog_store_clean                         = src['store_clean']
            obj.syslog_store_adblock                       = src['store_adblock']
            obj.syslog_store_privacy                       = src['store_privacy']
            obj.syslog_store_adult_heuristics              = src['store_adult_heuristics']
            obj.syslog_store_adult_safesearch              = src['store_adult_safesearch']
            obj.syslog_store_adult_youtube                 = src['store_adult_youtube']
            obj.syslog_store_adult_phrases                 = src['store_adult_phrases']
            obj.syslog_store_adult_image                   = src['store_adult_image']

            # some custom logic for categories
            if True:

                # set default value to true
                obj.syslog_store_categories = True

                # see if we need to reset it to false
                cat1 = src.get('store_categories', False)
                cat2 = src.get('store_categories_dynamic', False)
                cat3 = src.get('store_custom', False)

                if not (cat1 or cat2 or cat3):
                    obj.syslog_store_categories = False

            obj.syslog_store_http_sanitation               = src['store_http_sanitation']
            obj.syslog_store_content_content_type          = src['store_content_content_type']
            obj.syslog_store_content_charset               = src['store_content_charset']
            obj.syslog_store_content_transfer_encoding     = src['store_content_transfer_encoding']
            obj.syslog_store_content_file_name             = src['store_content_file_name']
            obj.syslog_store_content_file_type             = src['store_content_file_type']
            obj.syslog_store_content_file_size             = src['store_content_file_size']
            obj.syslog_store_apps                          = src['store_apps']
            obj.syslog_store_sslbump                       = src['store_sslbump']
            obj.syslog_store_path                          = src.get('store_path', False)
            obj.syslog_store_query                         = src.get('store_query', False)

        obj.update_interval         = data.get('update_interval', 5)
        obj.history_normalize_names = data.get('history_normalize_names', True)
        obj.history_anonymize_names = data.get('history_anonymize_names', False)

        if 'persistent' in data:

            src                                            = data['persistent']
            obj.persistent_enable                          = src['enable']
            obj.persistent_purge                           = src['purge']
            obj.persistent_store_clean                     = src['store_clean']
            obj.persistent_store_adblock                   = src['store_adblock']
            obj.persistent_store_privacy                   = src['store_privacy']
            obj.persistent_store_adult_heuristics          = src['store_adult_heuristics']
            obj.persistent_store_adult_safesearch          = src['store_adult_safesearch']
            obj.persistent_store_adult_youtube             = src['store_adult_youtube']
            obj.persistent_store_adult_phrases             = src['store_adult_phrases']
            obj.persistent_store_adult_image               = src['store_adult_image']

            # some custom logic for categories
            if True:

                # set default value to true
                obj.persistent_store_categories = True

                # see if we need to reset it to false
                cat1 = src.get('store_categories', False)
                cat2 = src.get('store_categories_dynamic', False)
                cat3 = src.get('store_custom', False)

                if not (cat1 or cat2 or cat3):
                    obj.persistent_store_categories = False

            obj.persistent_store_http_sanitation           = src['store_http_sanitation']
            obj.persistent_store_content_content_type      = src['store_content_content_type']
            obj.persistent_store_content_charset           = src['store_content_charset']
            obj.persistent_store_content_transfer_encoding = src['store_content_transfer_encoding']
            obj.persistent_store_content_file_name         = src['store_content_file_name']
            obj.persistent_store_content_file_type         = src['store_content_file_type']
            obj.persistent_store_content_file_size         = src['store_content_file_size']
            obj.persistent_store_apps                      = src['store_apps']
            obj.persistent_store_sslbump                   = src['store_sslbump']
            obj.persistent_store_path                      = src.get('store_path', False)
            obj.persistent_store_query                     = src.get('store_query', False)

        if 'accesslog' in data:

            src                                            = data['accesslog']
            obj.accesslog_enable                           = src['enable']
            obj.accesslog_store_clean                      = src['store_clean']
            obj.accesslog_store_adblock                    = src['store_adblock']
            obj.accesslog_store_privacy                    = src['store_privacy']
            obj.accesslog_store_adult_heuristics           = src['store_adult_heuristics']
            obj.accesslog_store_adult_safesearch           = src['store_adult_safesearch']
            obj.accesslog_store_adult_youtube              = src['store_adult_youtube']
            obj.accesslog_store_adult_phrases              = src['store_adult_phrases']
            obj.accesslog_store_adult_image                = src['store_adult_image']

            # some custom logic for categories
            if True:

                # set default value to true
                obj.accesslog_store_categories = True

                # see if we need to reset it to false
                cat1 = src.get('store_categories', False)
                cat2 = src.get('store_categories_dynamic', False)
                cat3 = src.get('store_custom', False)

                if not (cat1 or cat2 or cat3):
                    obj.accesslog_store_categories = False

            obj.accesslog_store_http_sanitation            = src['store_http_sanitation']
            obj.accesslog_store_content_content_type       = src['store_content_content_type']
            obj.accesslog_store_content_charset            = src['store_content_charset']
            obj.accesslog_store_content_transfer_encoding  = src['store_content_transfer_encoding']
            obj.accesslog_store_content_file_name          = src['store_content_file_name']
            obj.accesslog_store_content_file_type          = src['store_content_file_type']
            obj.accesslog_store_content_file_size          = src['store_content_file_size']
            obj.accesslog_store_apps                       = src['store_apps']
            obj.accesslog_store_sslbump                    = src['store_sslbump']
            obj.accesslog_store_path                       = src.get('store_path', False)
            obj.accesslog_store_query                      = src.get('store_query', False)

        if 'realtime' in data:

            src                                            = data['realtime']
            obj.realtime_enable                            = src['enable']
            obj.realtime_store_clean                       = src['store_clean']
            obj.realtime_store_adblock                     = src['store_adblock']
            obj.realtime_store_privacy                     = src['store_privacy']
            obj.realtime_store_adult_heuristics            = src['store_adult_heuristics']
            obj.realtime_store_adult_safesearch            = src['store_adult_safesearch']
            obj.realtime_store_adult_youtube               = src['store_adult_youtube']
            obj.realtime_store_adult_phrases               = src['store_adult_phrases']
            obj.realtime_store_adult_image                 = src['store_adult_image']

            # some custom logic for categories
            if True:

                # set default value to true
                obj.realtime_store_categories = True

                # see if we need to reset it to false
                cat1 = src.get('store_categories', False)
                cat2 = src.get('store_categories_dynamic', False)
                cat3 = src.get('store_custom', False)

                if not (cat1 or cat2 or cat3):
                    obj.realtime_store_categories = False
                    
            obj.realtime_store_http_sanitation             = src['store_http_sanitation']
            obj.realtime_store_content_content_type        = src['store_content_content_type']
            obj.realtime_store_content_charset             = src['store_content_charset']
            obj.realtime_store_content_transfer_encoding   = src['store_content_transfer_encoding']
            obj.realtime_store_content_file_name           = src['store_content_file_name']
            obj.realtime_store_content_file_type           = src['store_content_file_type']
            obj.realtime_store_content_file_size           = src['store_content_file_size']
            obj.realtime_store_apps                        = src['store_apps']
            obj.realtime_store_sslbump                     = src['store_sslbump']
            obj.realtime_store_path                        = src.get('store_path', True)
            obj.realtime_store_query                       = src.get('store_query', True)
            obj.realtime_limit_record_count                = src.get('limit_record_count', 10000)

        obj.save()
        