import os
import re

from django.db.models import Max
#
#
#
from _domain.utils import read_json_array, read_json_object

#
#
#
from safety.models import *
from squid.models import AuthAd

#
#
#
class NetworkImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "squid", "wsicap.json")
        if not os.path.exists(path):
            path = os.path.join(etc_dir, "network.json")

        if os.path.exists(path):
            self.upgrade_impl(read_json_object(path))

    def upgrade_impl(self, data):

        obj = Network.objects.first()

        obj.wsicap_address = data.get("icap_address", "127.0.0.1")   
        obj.wsicap_port    = data.get("icap_port", 1344)   
        obj.wsicap_threads = data.get("icap_threads", 9)   

        obj.save()
    
#
#
#
class AnnoyancesImporter:

    def upgrade(self, etc_dir):

        # import adblock
        path = os.path.join(etc_dir, "safety", "adblock.json")
        if not os.path.exists(path):
            path = os.path.join(etc_dir, "adblock.json")

        self.upgrade_adblock_impl(read_json_array(path))

        # import privacy
        path = os.path.join(etc_dir, "safety", "privacy.json")
        if not os.path.exists(path):
            path = os.path.join(etc_dir, "privacy.json")

        self.upgrade_privacy_impl(read_json_array(path))

        # now the new annoyances
        path = os.path.join(etc_dir, "safety", "subscriptions.json")
        if os.path.exists(path):
            self.upgrade_subscriptions(read_json_object(path))

    def upgrade_subscriptions(self, data):

        obj = Annoyances.objects.first()

        obj.apply_replace_heuristics    = data['apply_replace_heuristics']
        obj.replace_with_image          = data['replace_with_image']
        obj.hide_tags                   = data.get('hide_tags', True)        
        obj.mangle_id                   = data.get('mangle_id', False)
        obj.mangle_class                = data.get('mangle_class', False)        
        obj.scan_external_links         = data.get('scan_external_links', False)

        obj.save()


    def upgrade_adblock_impl(self, data):

        annoyances = Annoyances.objects.first()

        for subscription in data:

            if 'name' in subscription and 'enable' in subscription:

                attrname = "enable_%s" % subscription['name']
                if subscription['enable']:
                    setattr(annoyances, attrname, True)
                else:
                    setattr(annoyances, attrname, False)

        annoyances.save()

    def upgrade_privacy_impl(self, data):

        annoyances = Annoyances.objects.first()

        for subscription in data:

            if 'name' in subscription and 'enable' in subscription:

                attrname = "enable_%s" % subscription['name']
                if subscription['enable']:
                    setattr(annoyances, attrname, True)
                else:
                    setattr(annoyances, attrname, False)

        annoyances.save()

#
#
#
class BypassImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "safety", "bypass_tokens.json")
        if os.path.exists(path):
            self.upgrade_impl(read_json_array(path))

    def upgrade_impl(self, entries):

        for entry in entries:

            if not entry['value']:
                continue

            token, created = ByPassToken.objects.get_or_create(value=entry['value'])
            token.name     = entry['name']
            token.comment  = entry['comment']

            token.save()


#
#
#
class RecategorizedDomainsImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "safety", "recategorized_domains.json")
        if os.path.exists(path):
            self.upgrade_impl(read_json_array(path))

    def upgrade_impl(self, entries):

        for entry in entries:

            if not entry['domain']:
                continue

            domain, created = RecategorizedDomain.objects.get_or_create(name=entry['domain'])
            for category in entry['categories']:

                attrname = "assign_%s" % category
                setattr(domain, attrname, True)

            domain.save()


#
#
#
class TrustedCategoriesImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "safety", "trusted_categories.json")
        if os.path.exists(path):
            self.upgrade_impl(read_json_array(path))

    def upgrade_impl(self, entries):

        obj = Categories.objects.first()

        for entry in entries:

            attrname = "trust_%s" % entry
            setattr(obj, attrname, True)

        obj.save()




#
#
#
class AppsImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "safety", "apps.json")
        if not os.path.exists(path):
            path = os.path.join(etc_dir, "apps.json")

        self.upgrade_impl(read_json_object(path))

    def upgrade_impl(self, data):

        if 'google_apps_allowed_domains' in data:
            obj  = Apps.objects.first()
            obj.google_apps_allowed_domains = data['google_apps_allowed_domains']
            obj.save()

#
#
#
class CategoriesImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "safety", "categories.json")
        if not os.path.exists(path):
            return

        self.upgrade_impl(read_json_object(path))

    def upgrade_impl(self, data):

        obj = Categories.objects.first()
        obj.use_ml_domains = data.get("use_ml_domains", False)
        obj.save()



#
#
#
class AdultImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "safety", "adult.json")
        if not os.path.exists(path):
            path = os.path.join(etc_dir, "adult.json")

        self.upgrade_impl(read_json_object(path))

    def upgrade_impl(self, data):

        obj = PhraseEngine.objects.first()
        obj.count_type = data.get('count_type', PhraseEngine.PHRASE_ENGINE_COUNT_MULTIPLE)
        obj.save()


#
#
#
class LdapImporter:

    def upgrade(self, major, minor, etc_dir):

        if (major > 4) or (major == 4 and minor > 6):
            return self.upgrade_new(etc_dir)
        else:
            return self.upgrade_old(etc_dir)

    def upgrade_old(self, etc_dir):

        data = read_json_object(os.path.join(etc_dir, "ldap.json"))
        obj  = AuthAd.objects.first()

        if 'server' in data and 'schema' in data:

            obj.dc1addr = data['server']
            if data['schema'] == "ldaps":
                obj.use_ldaps = True

        if 'bind_user' in data and 'bind_pass' in data and 'basedn' in data:
            obj.bind_user = data['bind_user']
            obj.bind_pass = data['bind_pass']
            obj.base_dn   = data['basedn']
            obj.save()

        if 'cache_time' in data and 'timeout' in data:
            
            obj.cachetime = data['cache_time']
            obj.timeout   = data['timeout']
            obj.save()

    def upgrade_new(self, etc_dir):

        file = os.path.join(etc_dir, "squid", "auth_domain.json")
        if not os.path.isfile(file):
            return

        data = read_json_object(file)
        obj  = AuthAd.objects.first()

        obj.dc1addr   = data['dc1addr']
        obj.dc2addr   = data['dc2addr']
        obj.base_dn   = data['base_dn']
        obj.bind_user = data['bind_user']
        obj.bind_pass = data['bind_pass']
        obj.realm     = data['realm']

        if "use_ldaps" in data:
            if data["use_ldaps"]:
                obj.lookup_mode = AuthAd.LOOKUP_MODE_LDAPS
        else:
            port1 = data.get("dc1port", 389)
            port2 = data.get("dc2port", 389)

            if port1 == 389 or port2 == 389:
                obj.lookup_mode = AuthAd.LOOKUP_MODE_LDAP
            elif port1 == 636 or port2 == 636:
                obj.lookup_mode = AuthAd.LOOKUP_MODE_LDAPS
            elif port1 == 3268 or port2 == 3268:
                obj.lookup_mode = AuthAd.LOOKUP_MODE_GC
            elif port1 == 3269 or port2 == 3269:
                obj.lookup_mode = AuthAd.LOOKUP_MODE_GCS
            else:
                pass

        obj.save()

        data = read_json_object(os.path.join(etc_dir, "squid", "auth_group_membership.json"))
        
        obj.cachetime = data['cache_time']
        obj.timeout   = data['timeout']
        obj.save()

#
#
#
class MembersImporter:

    def __init__(self, policy):
        self.policy = policy

    def upgrade(self, major, minor, folder):

        self.upgrade_impl(major, minor, os.path.join(folder, "members"))

    def upgrade_impl(self, major, minor, folder):

        # normal items are simple
        for name, set in {
            'user_ip.json'         : self.policy.memberip_set,
            'user_ip6.json'        : self.policy.memberip_set,
            'user_ip_range.json'   : self.policy.memberrange_set,
            'user_ip6_range.json'  : self.policy.memberrange_set,
            'user_ip_subnet.json'  : self.policy.membersubnet_set,
            'user_ip6_subnet.json' : self.policy.membersubnet_set,
            'user_name.json'       : self.policy.membername_set,
        }.iteritems():

            file = os.path.join(folder, name)
            if os.path.exists(file ):
                items = read_json_array(file)
                for item in items:
                    if isinstance(item, basestring):
                        value   = item # in < 4.7
                        comment = ""
                    else:
                        value   = item.get("value", "")
                        comment = item.get("comment", "")

                    if len(value) > 0:
                        try:
                            v, c = set.get_or_create(value=value)
                            v.comment = comment
                            v.save()
                        except Exception as e:
                        	# logging.warning("Ignoring import of %s, error '%s' ..." % (value, str(e)))
                        	pass
                            

        # ldap needs to be parsed manually and differently in 4.6+
        for item in read_json_array(os.path.join(folder, 'user_ldap.json')):

            if (("%d.%d" % (major, minor)) in ["4.6", "4.7", "4.8", "4.9"]) or major >= 5:

                obj, created = self.policy.memberldap_set.get_or_create(dn=item["dn"])
                obj.name      = item["name"]
                obj.recursive = item["recursive"]
                if "comment" in item:
                    obj.comment = item["comment"]
                obj.save()

            else:

                test_str0 = "memberOf="
                test_str1 = "memberOf:1.2.840.113556.1.4.1941:="

                # determine recursiveness
                recursive = False
                pos = item.rfind(test_str1)
                if pos != -1:
                    recursive = True
                    pos      += len(test_str1)
                else:
                    pos = item.rfind(test_str0)
                    if pos == -1:
                        continue
                    else:
                        pos += len(test_str0)

                # determine dn
                dn = item[pos:]
                while dn.strip(')') != dn:
                    dn = dn.strip(')')

                # determine name
                matched = re.match(r'cn=(.*?),.*', dn, re.M|re.I)
                if matched:
                    group_name = matched.group(1)
                else:
                    group_name = "unknown"

                obj, created  = self.policy.memberldap_set.get_or_create(dn=dn)
                obj.name      = group_name
                obj.recursive = recursive
                obj.save()



#
#
#
class RulesImporter:

    def __init__(self, policy):
        self.policy  = policy

    def upgrade(self, major, minor, folder):

        self.upgrade_impl(folder)

    def upgrade_impl(self, folder):

        # adblock
        path = os.path.join(folder, "block_ads.json")
        if os.path.exists(path):

            data = read_json_object(path)
            obj  = self.policy.ruleannoyances
        
            obj.block_ads = data.get('block_ads', False)
            obj.save()

        # privacy
        path = os.path.join(folder, "protect_privacy.json")
        if os.path.exists(path):

            data = read_json_object(path)
            obj  = self.policy.ruleannoyances
        
            obj.protect_privacy = data.get('protect_privacy', False)
            obj.save()

        # new annoyances file
        path = os.path.join(folder, "block_annoyances.json")
        if os.path.exists(path):

            data = read_json_object(path)
            obj  = self.policy.ruleannoyances

            obj.block_ads       = data.get('block_ads', False)        
            obj.protect_privacy = data.get('protect_privacy', False)
            obj.save()

            obj = self.policy.ruleapps
            obj.hide_yt_comments    = data.get('hide_yt_comments', False)        
            obj.hide_yt_suggestions = data.get('hide_yt_suggestions', False)        
            obj.hide_yt_other       = data.get('hide_yt_other', False)        
            obj.save()

        # safe search may be in two places
        enable_safe_search = True

        # adult
        data = read_json_object(os.path.join(folder, "block_adult.json"))
        obj  = self.policy.ruleadult

        if 'enable_safe_search' in data:
            enable_safe_search = data['enable_safe_search']

        obj.enable_phrases            = data['fulltext_detection_enable']
        obj.phrases_maximum_weight    = data['fulltext_detection_maximum_weight']
        obj.phrases_maximum_size      = data['fulltext_detection_maximum_size']
        obj.fulltext_parse_links      = data.get('fulltext_parse_links', False)
        obj.fulltext_scan_css         = data.get('fulltext_scan_css', False)
        obj.fulltext_scan_javascript  = data.get('fulltext_scan_javascript', False)
        obj.fulltext_scan_links       = data.get('fulltext_scan_links', False)
        obj.enable_image_filtering    = data.get('enable_image_filtering', False)
        obj.heuristics_maximum_weight = data.get('heuristics_maximum_weight', 40)
        obj.trust_allowed_categories  = data.get('trust_allowed_categories', True)
        obj.enable_heuristics         = data['enable_heuristics']
        obj.save()

        # upgrade apps apps
        obj  = self.policy.ruleapps                        
        path = os.path.join(folder, "apps.json")
        if os.path.exists(path):
            data = read_json_object(path)

            if 'enable_safe_search' in data:
                enable_safe_search = data['enable_safe_search']

            obj.enable_google_apps  = data.get('enable_google_apps', False)
            obj.hide_yt_comments    = data.get('hide_yt_comments', False)
            obj.hide_yt_suggestions = data.get('hide_yt_suggestions', False)
            obj.hide_yt_other       = data.get('hide_yt_other', False)
            obj.enable_safe_search  = enable_safe_search
        
        obj.save()

        # normal items are simple
        for name, set in {
            'block_urls.json'         : self.policy.ruleurl_set, 
            'block_file_name.json'    : self.policy.rulefilename_set, 
            'block_file_content.json' : self.policy.rulefilecontent_set, 
            'block_domains.json'      : self.policy.ruledomain_set, 
            'block_content_type.json' : self.policy.rulecontenttype_set, 
            'block_charset.json'      : self.policy.rulecharset_set,
            'block_useragents.json'   : self.policy.ruleuseragent_set,
        }.iteritems():

            # only import if file exists
            path = os.path.join(folder, name)
            if not os.path.exists(path):
                continue

            items = read_json_array(path)
            for item in items:
                if isinstance(item, basestring):
                    value   = item # in < 4.7
                    comment = ""
                else:
                    value   = item.get("value", "")
                    comment = item.get("comment", "")

                if len(value) > 0:
                    try:
                        v, c = set.get_or_create(value=value)
                        v.comment = comment
                        v.save()
                    except Exception as e:
                        #logging.warning("Ignoring import of %s, error '%s' ..." % (value, str(e)))
                        pass

        # categories are a bit different
        if True:

            data = read_json_object(os.path.join(folder, 'block_categories.json'))
            rule = self.policy.rulecategory


            if 'block_noncategorized_domains' in data:
                rule.block_noncategorized_domains = data['block_noncategorized_domains']

            items = None
            if 'blocked_categories' in data:
                items = data['blocked_categories']
            else:
                items = data

            for item in items:
                setattr(rule, "block_%s" % name, True)

            rule.save()

        # dynamic categories are different too
        if True:

            data = read_json_object(os.path.join(folder, 'dynamic_categorization.json'))

            rule = self.policy.ruledynamiccategory
            rule.enabled          = data.get('enabled', True)
            rule.analyze_request  = data.get('analyze_request', True)
            rule.analyze_response = data.get('analyze_response', True)
            rule.classify_type    = data.get('classify_type', RuleDynamicCategory.CLASSIFY_UNKNOWN_AND_UNTRUSTED)

            if 'classifiers' in data:
                items = data['classifiers']
                for item in items:
                    setattr(rule, "classify_%s" % name, True)

            rule.save()
        
        # custom categories are even more different
        for name, obj in {
            'block_categories_custom.json' : self.policy.rulecategorycustom_set
        }.iteritems():
            for item in read_json_array(os.path.join(folder, name)):
                (category, created) = CustomCategory.objects.get_or_create(name=item)
                obj.get_or_create(category=category.name, enable=True)

        # block file size
        obj  = self.policy.rulefilesize
        path = os.path.join(folder, "block_file_size.json")
        if os.path.exists(path):
            data = read_json_object(path)
            obj.enable   = data.get('enable', False)
            obj.max_size = data.get('max_size', 1048576)

        obj.save()

#
#
#
class ExclusionsImporter:

    def __init__(self, policy):
        self.policy  = policy

    def upgrade(self, major, minor, folder):

        self.upgrade_impl(os.path.join(folder, "exclusions"))

    
    def upgrade_impl(self, folder):

        # loop through all the exclusions
        for n, s in {
            "content_type.json"     : self.policy.exclusioncontenttype_set,
            "domain_ip.json"        : self.policy.exclusionip_set,
            "domain_ip_range.json"  : self.policy.exclusionrange_set,
            "domain_ip_subnet.json" : self.policy.exclusionsubnet_set,
            "request_uri.json"      : self.policy.exclusionurl_set,
            "domain_name.json"      : self.policy.exclusiondomain_set,
        }.iteritems():

            # load json array
            for data in read_json_object(os.path.join(folder, n)):

                if isinstance(data, basestring):
                    obj, created = s.get_or_create(value=data)
                else:
                    # create or get existing one
                    obj, created = s.get_or_create(value=data['value'])

                    # set scan flags for it
                    obj.scan_adult      = data['scan']['adult']
                    obj.scan_categories = data['scan']['categories']
                    obj.scan_file       = data['scan']['file']
                    obj.scan_adblock    = data['scan']['adblock']
                    obj.scan_privacy    = data['scan']['privacy']
                    obj.scan_http       = data['scan']['http']

                    # save comment
                    if 'comment' in data:
                        obj.comment = data["comment"]

                    # and save the object
                    obj.save()

#
#
#
class PolicyImporter:

    def __init__(self, policy):

        self.policy  = policy

    def upgrade(self, major, minor, folder):

        self.upgrade_globals(major, minor, folder)
        self.upgrade_schedule(major, minor, folder)
        self.upgrade_bypass(major, minor, folder)


        u = ExclusionsImporter(self.policy)
        u.upgrade(major, minor, folder)

        u = MembersImporter(self.policy)
        u.upgrade(major, minor, folder)

        u = RulesImporter(self.policy)
        u.upgrade(major, minor, os.path.join(folder, "rules"))

    def upgrade_globals(self, major, minor, folder):

        if major < 4:
            return

        data     = read_json_object(os.path.join(folder, "policy.json"))
        advanced = self.policy.advanced

        advanced.comment          = data.get('description', "")
        advanced.enable           = data.get('enabled', True)
        advanced.hide_history     = data.get('hide_history', False)
        advanced.hide_result_info = data.get('hide_result_info', True)
        advanced.ignore_case      = data.get('ignore_case_exclusions', True)
        advanced.sslbump          = data.get('sslbump', True)
        advanced.tunnel_block     = data.get('tunnel_block', True)


        path1 = os.path.join(folder, "advanced.json")
        if os.path.exists(path1):
            advanced.exclude_by_referer = read_json_object(path1).get('exclude_by_referer', False)

        advanced.save()

    def upgrade_bypass(self, major, minor, folder):

        data = read_json_object(os.path.join(folder, "policy.json"))

        self.policy.bypass_allowed        = data.get("bypass_allowed", False)
        self.policy.bypass_strip_www      = data.get("bypass_strip_www", True)
        self.policy.bypass_children       = data.get("bypass_children", True)
        # self.policy.bypass_category     = data.get("bypass_category", False) # not implemented
        # self.policy.bypass_all          = data.get("bypass_all", False)      # not implemented
        self.policy.bypass_referers       = data.get("bypass_referers", False)
        self.policy.bypass_duration       = data.get("bypass_duration", 60)
        self.policy.bypass_token_required = data.get("bypass_token_required", False)

        self.policy.bypass_adult          = data.get("bypass_adult", True)
        self.policy.bypass_categories     = data.get("bypass_categories", True)
        self.policy.bypass_file           = data.get("bypass_file", True)
        self.policy.bypass_adblock        = data.get("bypass_adblock", True)
        self.policy.bypass_privacy        = data.get("bypass_privacy", True)
        self.policy.bypass_http           = data.get("bypass_http", True)


    def upgrade_schedule(self, major, minor, folder):

        if major < 4:
        	if major == 4 and minor < 9:
        		return

        data      = read_json_object(os.path.join(folder, "schedule.json"))
        schedules = self.policy.schedule_set

        for item in data:

            schedules.create(
                on_mon = item['days']['mon'],
                on_tue = item['days']['tue'],
                on_wed = item['days']['wed'],
                on_thu = item['days']['thu'],
                on_fri = item['days']['fri'],
                on_sat = item['days']['sat'],
                on_sun = item['days']['sun'],
                from_hours = item['from']['hours'],
                from_mins  = item['from']['minutes'],
                to_hours   = item['to']['hours'],
                to_mins    = item['to']['minutes']
            )


#
#
#
class PoliciesImporter:

    def upgrade(self, major, minor, etc_dir):

        folder = os.path.join(etc_dir, "safety", "policies")
        if not os.path.isdir(folder):
            folder = os.path.join(etc_dir, "policies")

        # the list of (name, folder, priority) tuples
        policies = []

        # enumerate
        default_policy = None
        for name in os.listdir(folder):

            # policy folder
            policy_dir = os.path.join(folder, name)
            if os.path.isdir(policy_dir):

                if name == 'default':
                    default_policy = (name, policy_dir, 0)
                else:
                    policies.append( (name, policy_dir, self.get_priority(policy_dir)) )

        # now we sort the list from lowest to highest priority 
        policies.sort(key=lambda tup: tup[2]) 

        if major == 3:
            policies.reverse()

        # prepend the default item
        if default_policy != None:
            policies.insert(0, default_policy)

        # by doing normal index enumeration we automatically get policies in correct priority order
        for (n, f, p) in policies:
            self.upgrade_policy(major, minor, f, n)

    def get_priority(self, policy_dir):
        j = os.path.join(policy_dir, "policy.json")
        if os.path.exists(j):
            d = read_json_object(j)
            return d['priority']

        j = os.path.join(policy_dir, "policy.conf")
        if os.path.exists(j):
            store    = Storage(ConfFileReader(j).read_lines(True))
            priority = store.get_int('priority')
            if priority != 0:
                return priority

        return 1

    def create_policy(self, name):

        # get current maximum priority
        max_priority = Policy.objects.all().aggregate(Max('priority'))['priority__max']

        # create and save the policy
        policy = Policy.objects.create(name=name, priority=max_priority+1)
        policy.save()
        
        # create corresponding one-to-one rules
        policy.advanced = Advanced(policy=policy, enable=True, comment="Imported filtering policy. Specify meaningful comment here. Please adjust this policy settings and enable it afterwards.")
        policy.advanced.save()
        
        policy.schedule = Schedule(policy=policy)
        policy.schedule.save()
        
        policy.ruleannoyances = RuleAnnoyances(policy=policy)
        policy.ruleannoyances.save()
        
        policy.ruleadult = RuleAdult(policy=policy)
        policy.ruleadult.save()
        
        policy.ruleapps = RuleApps(policy=policy)
        policy.ruleapps.save()

        policy.rulefilesize = RuleFileSize(policy=policy)
        policy.rulefilesize.save()

        policy.rulecategory = RuleCategory(policy=policy)
        policy.rulecategory.save()

        policy.ruledynamiccategory = RuleDynamicCategory(policy=policy)
        policy.ruledynamiccategory.save()

        return policy

    def upgrade_policy(self, major, minor, policy_dir, name):

        policy = None
        try:
            items = Policy.objects.filter(name=name)
            if len(items) > 0:
                policy = items[0]
            else:
                raise Policy.DoesNotExist()

        except Policy.DoesNotExist:        
            if name == 'default':
                raise Exception("Cannot find policy '%s' (default) - it must always exist!" % name)
            policy = self.create_policy(name)

        u = PolicyImporter(policy)
        u.upgrade(major, minor, policy_dir)

        policy.save()


#
#
#
class Upgrader(object):

    def __init__(self, major, minor):

        self.major   = major
        self.minor   = minor

    def upgrade(self, etc_dir):

        NetworkImporter().upgrade(etc_dir)
        AnnoyancesImporter().upgrade(etc_dir)
        AppsImporter().upgrade(etc_dir)
        AdultImporter().upgrade(etc_dir)
        BypassImporter().upgrade(etc_dir)
        RecategorizedDomainsImporter().upgrade(etc_dir)
        TrustedCategoriesImporter().upgrade(etc_dir)
        CategoriesImporter().upgrade(etc_dir)
        LdapImporter().upgrade(self.major, self.minor, etc_dir)
        PoliciesImporter().upgrade(self.major, self.minor, etc_dir)

    
