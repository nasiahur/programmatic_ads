#
#
#
import os
import shutil

#
# domain
#
from _domain.utils import FileWriter, JsonDumper

#
#
#
from utility.generator import BaseGenerator

#
#
#
from safety.models import *
from squid.models import BumpMode, ExcludeCategories

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

    #
    #
    #
    def generate_config(self, target_dir):

        # create writer and dumper
        w = FileWriter(target_dir)        
        d = JsonDumper()

        # generate all global files
        self.generate_network(w, d)
        self.generate_apps(w, d)
        self.generate_subscriptions(w, d)
        self.generate_trusted_categories(w, d)
        self.generate_recategorized_domains(w, d)
        self.generate_skip_sslbump(w, d)
        self.generate_engine(w, d)
        self.generate_bypass_tokens(w, d)
        
        # now generate policies
        self.generate_policies(target_dir)

    #
    #
    #
    def generate_network(self, writer, dumper):

        o = Network.objects.first()
        d = {
            "icap_address": o.wsicap_address, 
            "icap_debug"  : o.wsicap_debug, 
            "icap_port"   : str(o.wsicap_port),
            "icap_threads": o.wsicap_threads,
            "icap_logging": o.wsicap_logging
        }
        writer.write('wsicap.json', dumper.dumps(d))


    #
    #
    #
    def generate_apps(self, writer, dumper):
        o = Apps.objects.first()
        d = {
            'google_apps_allowed_domains' : o.google_apps_allowed_domains
        }
        writer.write('apps.json', dumper.dumps(d))

    #
    #
    #
    def generate_subscriptions(self, writer, dumper):

        # generate advanced
        if True:

            o = Annoyances.objects.first()
            d = {
                'apply_replace_heuristics' : o.apply_replace_heuristics,
                'replace_with_image'       : o.replace_with_image,
                'hide_tags'                : o.hide_tags,
                'scan_external_links'      : o.scan_external_links,
                'mangle_id'                : o.mangle_id,
                'mangle_class'             : o.mangle_class
            }
            writer.write('subscriptions.json', dumper.dumps(d))


        # generate adblock
        array   = []
        adblock = Annoyances.objects.first()

        array.append({ 'name': 'bulgarian', 'enable': adblock.enable_bulgarian})
        array.append({ 'name': 'chinese', 'enable': adblock.enable_chinese})                
        array.append({ 'name': 'czech', 'enable': adblock.enable_czech})        
        array.append({ 'name': 'danish', 'enable': adblock.enable_danish})        
        array.append({ 'name': 'dutch', 'enable': adblock.enable_dutch})
        array.append({ 'name': 'english', 'enable': adblock.enable_english})
        array.append({ 'name': 'estonian', 'enable': adblock.enable_estonian})        
        array.append({ 'name': 'french', 'enable': adblock.enable_french})
        array.append({ 'name': 'german', 'enable': adblock.enable_german})
        array.append({ 'name': 'greek', 'enable': adblock.enable_greek})
        array.append({ 'name': 'hungarian', 'enable': adblock.enable_hungarian})
        array.append({ 'name': 'indian', 'enable': adblock.enable_indian})
        array.append({ 'name': 'israeli', 'enable': adblock.enable_israeli})
        array.append({ 'name': 'italian', 'enable': adblock.enable_italian})
        array.append({ 'name': 'japanese', 'enable': adblock.enable_japanese})
        array.append({ 'name': 'korean', 'enable': adblock.enable_korean})
        array.append({ 'name': 'latvian', 'enable': adblock.enable_latvian})
        array.append({ 'name': 'lithuanian', 'enable': adblock.enable_lithuanian})
        array.append({ 'name': 'polish', 'enable': adblock.enable_polish})
        array.append({ 'name': 'portuguese', 'enable': adblock.enable_portuguese})
        array.append({ 'name': 'romanian', 'enable': adblock.enable_romanian})
        array.append({ 'name': 'russian', 'enable': adblock.enable_russian})
        array.append({ 'name': 'slovak', 'enable': adblock.enable_slovak})
        array.append({ 'name': 'spanish', 'enable': adblock.enable_spanish})
        array.append({ 'name': 'swedish', 'enable': adblock.enable_swedish})
        array.append({ 'name': 'turkish', 'enable': adblock.enable_turkish})
        array.append({ 'name': 'vietnamese', 'enable': adblock.enable_vietnamese})
        array.append({ 'name': 'custom', 'enable': adblock.enable_custom1})

        writer.write('adblock.json', dumper.dumps(array))

        # now generate the privacy
        array   = []
        privacy = Annoyances.objects.first()

        array.append({ 'name': 'adware', 'enable': privacy.enable_adware})
        array.append({ 'name': 'annoyance', 'enable': privacy.enable_annoyance})
        array.append({ 'name': 'antiadb', 'enable': privacy.enable_antiadb})
        array.append({ 'name': 'cookies', 'enable': privacy.enable_cookies})
        array.append({ 'name': 'privacy', 'enable': privacy.enable_privacy})
        array.append({ 'name': 'social', 'enable': privacy.enable_social})
        array.append({ 'name': 'tracking', 'enable': privacy.enable_tracking})
        array.append({ 'name': 'custom', 'enable': privacy.enable_custom2})

        writer.write('privacy.json', dumper.dumps(array))

        

    #
    #
    #
    def generate_bypass_tokens(self, writer, dumper):
        
        for (name, collection) in [ 
            ('bypass_tokens.json', ByPassToken.objects),             
        ]:
            array = []
            for item in collection.all():
                array.append({ 'name': item.name, 'value': item.value, 'comment': item.comment })

            writer.write(name, dumper.dumps(array))


    #
    #
    #
    def generate_recategorized_domains(self, writer, dumper):

        # this is the array of recategorized domains
        array = []

        # take each recategorized domain
        for item in RecategorizedDomain.objects.all(): 

            # and append it as dict
            array.append(
                { 
                    "domain"     : item.name, 
                    "categories" : item.categories_as_array() 
                }
            )

        writer.write('recategorized_domains.json', dumper.dumps(array))

    def generate_trusted_categories(self, writer, dumper):

        categories = Categories.objects.first()

        # generate categories
        data = {
            'use_ml_domains' : categories.use_ml_domains
        }
        writer.write('categories.json', dumper.dumps(data))

        # generate trusted categories
        array = categories.categories_as_array()
        
        writer.write('trusted_categories.json', dumper.dumps(array))


    #
    #
    #
    def generate_skip_sslbump(self, writer, dumper):

        bumpmode = BumpMode.objects.first()
        d = {
            'bump_all' : bumpmode.value,            
        }
        writer.write('ssl_bump.json', dumper.dumps(d))

        # get the skil ssl bump object from squid
        array = ExcludeCategories.objects.first().categories_as_array()

        # and dump iit
        writer.write('non_bumped_categories.json', dumper.dumps(array))

    #
    #
    #
    def generate_engine(self, writer, dumper):
        o = PhraseEngine.objects.first()
        d = {
            'count_type' : o.count_type
        }
        writer.write('adult.json', dumper.dumps(d))
        
    #
    #
    #
    def generate_policies(self, target_dir):
    
        policies_cur = os.path.join(target_dir, "policies")
        policies_new = os.path.join(target_dir, "policies.new")
        policies_bak = os.path.join(target_dir, "policies.bak")

        # now create folder for policies
        self.recreate_dir(policies_new)
        
        # generate all artifacs for each policy
        for policy in Policy.objects.all():
            
            # construct new policies folder name
            policy_dir = os.path.join(policies_new, policy.name)
            
            # recreate this new folder
            self.recreate_dir(policy_dir)
            
            # generate a policy into this new dir
            self.generate_policy(policy_dir, policy)

        # copy current policies into backup
        if os.path.exists(policies_bak):
            shutil.rmtree(policies_bak)
        
        # move the policies from .new
        if os.path.exists(policies_cur):
            shutil.copytree(policies_cur, policies_bak)
            shutil.rmtree(policies_cur)
            
        shutil.move(policies_new, policies_cur)


    def generate_schedule(self, policy_dir, policy):

        # generate schedule array
        s = []
        for schedule in policy.schedule_set.all():
            s.append({
                "days": {
                    "mon" : schedule.on_mon,
                    "tue" : schedule.on_tue,
                    "wed" : schedule.on_wed,
                    "thu" : schedule.on_thu,
                    "fri" : schedule.on_fri,
                    "sat" : schedule.on_sat,
                    "sun" : schedule.on_sun
                }, 
                "from": {
                    "hours": schedule.from_hours,
                    "minutes": schedule.from_mins
                },
                "to": {
                    "hours": schedule.to_hours,
                    "minutes": schedule.to_mins
                }
            })

        # create writer and dumper
        w = FileWriter(policy_dir)        
        d = JsonDumper()
        
        # write and dump        
        w.write('schedule.json', d.dumps(s))
        
    #
    #
    #
    def generate_policy(self, policy_dir, policy):

        # first generate the schedule
        self.generate_schedule(policy_dir, policy)

        # now generate the policy    
        o = policy
        a = {
            "enabled"                      : o.advanced.enable,
            "priority"                     : o.priority,
            "ignore_case_exclusions"       : o.advanced.ignore_case,
            "ignore_case_members"          : o.advanced.ignore_case,
            "ignore_case_rules"            : o.advanced.ignore_case,
            "use_url_as_filename"          : True,
            "description"                  : o.advanced.comment,
            "hide_history"                 : o.advanced.hide_history,
            "hide_result_info"             : o.advanced.hide_result_info,
            "sslbump"                      : o.advanced.sslbump,
            "tunnel_block"                 : o.advanced.tunnel_block,

            # bypass settings
            "bypass_allowed"               : o.bypass_allowed,
            "bypass_strip_www"             : o.bypass_strip_www,
            "bypass_children"              : o.bypass_children,
            "bypass_referers"              : o.bypass_referers,
            "bypass_duration"              : o.bypass_duration,
            "bypass_token_required"        : o.bypass_token_required,
            "bypass_adult"                 : o.bypass_adult,
            "bypass_categories"            : o.bypass_categories,
            "bypass_file"                  : o.bypass_file,
            "bypass_adblock"               : o.bypass_adblock,
            "bypass_privacy"               : o.bypass_privacy,
            "bypass_http"                  : o.bypass_http
        }
        
        # create writer and dumper
        w = FileWriter(policy_dir)        
        d = JsonDumper()
        
        # write and dump        
        w.write('policy.json', d.dumps(a))
        
        # now generate policy components
        self.generate_members(policy_dir, policy)
        self.generate_exclusions(policy_dir, policy)
        self.generate_rules(policy_dir, policy)
        
    #
    #
    #
    def generate_members(self, policy_dir, policy):

        # construct the dir name
        dir = os.path.join(policy_dir, "members")
        
        # recreate it
        self.recreate_dir(dir)
        
        # create writer and dumper
        w = FileWriter(dir)
        j = JsonDumper()
        
        # write and dump
        for (n, v) in [
            ('user_ip.json', policy.memberip_set),
            ('user_name.json', policy.membername_set),
            ('user_ip_range.json', policy.memberrange_set),
            ('user_ip_subnet.json', policy.membersubnet_set)            
        ]: w.write(n, j.dumps(self.to_array(v.all())))
        
        # construct ldap groups out of single ldap server and group dns
        groups = []
        for group in policy.memberldap_set.all():
            groups.append({
                "name"      : group.name,
                "dn"        : group.dn,
                "recursive" : group.recursive,
                "comment"   : group.comment
            })

        w.write('user_ldap.json', j.dumps(groups))

    #
    #
    #
    def generate_exclusions(self, policy_dir, policy):

        # construct the dir name
        dir = os.path.join(policy_dir, "exclusions")
        
        # create it
        self.recreate_dir(dir)
        
        # create writer and dumper
        w = FileWriter(dir)
        j = JsonDumper()
        
        # write and dump
        for (n, v) in [
            ('domain_name.json', policy.exclusiondomain_set),
            ('domain_ip.json', policy.exclusionip_set),            
            ('content_type.json', policy.exclusioncontenttype_set),
            ('domain_ip_range.json', policy.exclusionrange_set),
            ('domain_ip_subnet.json', policy.exclusionsubnet_set),
            ('request_uri.json', policy.exclusionurl_set)
        ]: 
            array   = []
            objects = v.all()        
            
            for object in objects:
                array.append({
                    "value": object.value,
                    "comment": object.comment,
                    "scan" : {
                        "adult": object.scan_adult,
                        "categories": object.scan_categories,
                        "file": object.scan_file,
                        "adblock": object.scan_adblock,
                        "privacy": object.scan_privacy,
                        "http": object.scan_http,
                    }
                })
            w.write(n, j.dumps(array))

        # and also advanced
        w.write('advanced.json', j.dumps({"exclude_by_referer" : policy.advanced.exclude_by_referer}))
        
        
     
    #
    #
    #
    def generate_rules(self, policy_dir, policy):
    
        # construct rules folder
        rules_dir = os.path.join(policy_dir, "rules")
        
        # recreate it
        self.recreate_dir(rules_dir)
        
        # create writer and dumper
        w = FileWriter(rules_dir)
        j = JsonDumper()
        
        # call individual generators
        self.generate_ruleannoyances(rules_dir, policy.ruleannoyances, policy.ruleapps)
        self.generate_ruleadult(rules_dir, policy.ruleadult)
        self.generate_ruleapps(rules_dir, policy.ruleapps)
        self.generate_rulefilesize(rules_dir, policy.rulefilesize)
        self.generate_rule_dynamic_categorization(rules_dir, policy)
        
        # write different file types
        for (n,t) in [
            ('block_domains.json',      policy.ruledomain_set),
            ('block_urls.json',         policy.ruleurl_set),
            ('block_useragents.json',   policy.ruleuseragent_set),
            ('block_content_type.json', policy.rulecontenttype_set),
            ('block_file_name.json',    policy.rulefilename_set),
            ('block_file_content.json', policy.rulefilecontent_set),
            ('block_charset.json',      policy.rulecharset_set),
        ]: w.write(n, j.dumps(self.to_array(t.all())))
        
        # write blocked categories
        w.write('block_categories.json', j.dumps(
            {
                "block_noncategorized_domains" : policy.rulecategory.block_noncategorized_domains,
                "blocked_categories"           : policy.rulecategory.categories_as_array()
            }
        ))
        
        # write custom categories
        array = []
        for r in policy.rulecategorycustom_set.filter(enable=True):
            array.append(r.category)
        
        w.write('block_categories_custom.json', j.dumps(array))
        
    def generate_ruleannoyances(self, rules_dir, rule1, rule2):

        o1 = rule1  # annoyances
        o2 = rule2  # apps
        d  = {
            "block_ads"           : o1.block_ads,
            "protect_privacy"     : o1.protect_privacy,
            "hide_yt_comments"    : o2.hide_yt_comments,
            "hide_yt_suggestions" : o2.hide_yt_suggestions,
            "hide_yt_other"       : o2.hide_yt_other
        }
        FileWriter(rules_dir).write('block_annoyances.json', JsonDumper().dumps(d))
        
    def generate_ruleadult(self, rules_dir, rule):
        o = rule
        d = { 
            "trust_allowed_categories"          : o.trust_allowed_categories,
            "enable_heuristics"                 : o.enable_heuristics,
            "heuristics_maximum_weight"         : o.heuristics_maximum_weight,
            "fulltext_detection_enable"         : o.enable_phrases,
            "fulltext_detection_maximum_weight" : o.phrases_maximum_weight,
            "fulltext_detection_maximum_size"   : o.phrases_maximum_size,
            "fulltext_scan_links"               : o.phrases_scan_links, 
            "fulltext_scan_javascript"          : o.phrases_scan_javascript, 
            "fulltext_scan_css"                 : o.phrases_scan_css, 
            "fulltext_parse_links"              : o.phrases_parse_links, 
            "enable_image_filtering"            : o.enable_image_filtering
        }
        FileWriter(rules_dir).write('block_adult.json', JsonDumper().dumps(d))
        
    def generate_ruleapps(self, rules_dir, rule):
        o = rule
        d = { 
            "enable_google_apps"       : o.enable_google_apps,
            "enable_safe_search"       : o.enable_safe_search,
            "youtube_restrictions"     : o.youtube_restrictions            
        }
        FileWriter(rules_dir).write('apps.json', JsonDumper().dumps(d))

    def generate_rule_dynamic_categorization(self, rules_dir, policy):

        o = policy.ruledynamiccategory        
        d = {
            "enabled"          : o.enabled,
            "analyze_request"  : o.analyze_request,
            "analyze_response" : o.analyze_response,
            "classify_type"    : o.classify_type,
            "classifiers"      : o.categories_as_array(),
            "token_proximity"  : 4,		# hardcoded and is NOT visible in UI
            "check_delimiters" : True,  # hardcoded and is NOT visible in UI
            "probability"      : 40		# hardcoded and is NOT visible in UI

        }
        FileWriter(rules_dir).write('dynamic_categorization.json', JsonDumper().dumps(d))


    def generate_rulefilesize(self, rules_dir, rule):
        o = rule
        d = { 
            "enable"   : o.enable,
            "max_size" : o.max_size
        }
        FileWriter(rules_dir).write('block_file_size.json', JsonDumper().dumps(d))

    
        
    #
    #
    #
    def recreate_dir(self, dir_name):
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)
            
    #
    #
    #
    def to_array(self, objects):
        array = []
        for obj in objects:
            array.append( { "value": obj.value, "comment": obj.comment } )
        return array
   
