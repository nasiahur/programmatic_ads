#
# django
#
from django.db import models

#
# our
#
from _domain.utils import LicenseManager
from _domain.safety import BuildInCategories

#
#
#
class Safety(models.Model):

    def get_uicolor(self):

        try:
            (result, license) = LicenseManager().get()

            if result is True:

                if license['valid'] == "1":

                    if license['type'] == "community":

                        # updated the flag (used in views!)
                        self.is_community = True

                        # and return the community color
                        return 'black-blue'

                    if license['expires_soon'] == "1":
                        return 'cyan'
                    else:
                        return 'default'

        except Exception as e:
            pass

        return 'red'

    





#
#
#
class Network(models.Model):

    enable_icap        = models.BooleanField(default=True)                 # sets icap_enable on|off
    bypass_to_localnet = models.BooleanField(default=True)                 # connections to hosts in our LAN does not need to be filtered

    WSICAP_LOG_DEBUG   = 0
    WSICAP_LOG_INFO    = 1
    WSICAP_LOG_WARN    = 2
    WSICAP_LOG_ERROR   = 3
    WSICAP_LOG_CHOICES = (
        (WSICAP_LOG_DEBUG, "debug"),
        (WSICAP_LOG_INFO,  "info"),
        (WSICAP_LOG_WARN,  "warning"),
        (WSICAP_LOG_ERROR, "error")
    )

    wsicap_address = models.CharField(max_length=200, default="127.0.0.1") # address of ICAP server for web safety
    wsicap_port    = models.IntegerField(default=1344)                     # port
    wsicap_debug   = models.BooleanField(default=False)                    # special debug mode of web safety when it dumps ICAP req/resp contents on disk   
    wsicap_threads = models.IntegerField(default=9)
    wsicap_logging = models.IntegerField(choices=WSICAP_LOG_CHOICES,default=WSICAP_LOG_INFO)


#
#
#
class Apps(models.Model):    
    google_apps_allowed_domains = models.CharField(max_length=254, blank=True, unique=True)

#
#
#
class Annoyances(models.Model):

    # general settings
    apply_replace_heuristics = models.BooleanField(default=True)
    replace_with_image       = models.BooleanField(default=True)
    hide_tags                = models.BooleanField(default=True)
    mangle_id                = models.BooleanField(default=False)
    mangle_class             = models.BooleanField(default=False)
    scan_external_links      = models.BooleanField(default=False)

    # adblock subscriptions
    enable_bulgarian         = models.BooleanField(default=False)
    enable_chinese           = models.BooleanField(default=False)
    enable_czech             = models.BooleanField(default=False)
    enable_danish            = models.BooleanField(default=False)
    enable_dutch             = models.BooleanField(default=False)
    enable_english           = models.BooleanField(default=True)
    enable_estonian          = models.BooleanField(default=False)
    enable_french            = models.BooleanField(default=False)
    enable_german            = models.BooleanField(default=False)
    enable_greek             = models.BooleanField(default=False)
    enable_hungarian         = models.BooleanField(default=False)
    enable_indian            = models.BooleanField(default=False)
    enable_israeli           = models.BooleanField(default=False)
    enable_italian           = models.BooleanField(default=False)
    enable_japanese          = models.BooleanField(default=False)
    enable_korean            = models.BooleanField(default=False)
    enable_latvian           = models.BooleanField(default=False)
    enable_lithuanian        = models.BooleanField(default=False)
    enable_polish            = models.BooleanField(default=False)
    enable_portuguese        = models.BooleanField(default=False)
    enable_romanian          = models.BooleanField(default=False)
    enable_russian           = models.BooleanField(default=False)
    enable_slovak            = models.BooleanField(default=False)
    enable_spanish           = models.BooleanField(default=False)
    enable_swedish           = models.BooleanField(default=False)
    enable_turkish           = models.BooleanField(default=False)
    enable_vietnamese        = models.BooleanField(default=False)

    # privacy subscriptions
    enable_adware            = models.BooleanField(default=False)
    enable_annoyance         = models.BooleanField(default=False)
    enable_antiadb           = models.BooleanField(default=False)
    enable_cookies           = models.BooleanField(default=False)
    enable_privacy           = models.BooleanField(default=False)
    enable_social            = models.BooleanField(default=False)
    enable_tracking          = models.BooleanField(default=False)
    
    # youtube subscriptions
    enable_yt_comments       = models.BooleanField(default=False)
    enable_yt_suggestions    = models.BooleanField(default=False)
    enable_yt_other          = models.BooleanField(default=False)

    # custom subscriptions
    enable_custom1           = models.BooleanField(default=True)
    enable_custom2           = models.BooleanField(default=True)    

#
#
#
class CustomCategory(models.Model):

    class Meta:
        ordering = ["name"]

    name     = models.CharField(max_length=254, primary_key=True, unique=True)
    title    = models.CharField(max_length=254)
    trust    = models.BooleanField(default=False)   # the category may be marked as trusted (i.e. skip adult language detection on it)
    sslbump  = models.BooleanField(default=True)    # the category may be marked as non bumpable (i.e. skip SSL bump on it)

    def __unicode__(self):
        return self.title

#
#
#
class Categories(models.Model):

    use_ml_domains                     = models.BooleanField(default=False) # shall we load domains.dat or domains.ml.dat in the engine

    trust_adult_themes_sexuality       = models.BooleanField(default=False)
    trust_advertising                  = models.BooleanField(default=True)
    trust_alcohol_tobacco              = models.BooleanField(default=False)
    trust_anime_manga_webcomic         = models.BooleanField(default=False)
    trust_arts_society_culture         = models.BooleanField(default=False)
    trust_automotive                   = models.BooleanField(default=True)
    trust_banking_insurance_finance    = models.BooleanField(default=True)
    trust_blogs_personal               = models.BooleanField(default=False)
    trust_business_services_industry   = models.BooleanField(default=True)
    trust_classifieds_auctions         = models.BooleanField(default=False)
    trust_content_delivery_networks    = models.BooleanField(default=False)
    trust_cracks_hacking_illegal       = models.BooleanField(default=False)
    trust_dating                       = models.BooleanField(default=False)
    trust_drugs                        = models.BooleanField(default=False)
    trust_ecommerce_shopping           = models.BooleanField(default=True)
    trust_education_science_research   = models.BooleanField(default=True)
    trust_entertainment_humor_hobby    = models.BooleanField(default=False)
    trust_expired_parked               = models.BooleanField(default=False)
    trust_fashion_beauty_cosmetics     = models.BooleanField(default=True)
    trust_file_storage                 = models.BooleanField(default=False)
    trust_food_dining_restaurants      = models.BooleanField(default=True)
    trust_forums_message_boards        = models.BooleanField(default=False)
    trust_gambling                     = models.BooleanField(default=False)
    trust_games                        = models.BooleanField(default=False)
    trust_generic_non_categorized      = models.BooleanField(default=False)
    trust_government                   = models.BooleanField(default=True)
    trust_hate_discrimination_violence = models.BooleanField(default=False)
    trust_health_medicine_fitness      = models.BooleanField(default=True)
    trust_jobs_employment_career       = models.BooleanField(default=True)
    trust_messaging_chat               = models.BooleanField(default=False)
    trust_movies                       = models.BooleanField(default=True)
    trust_music_radio                  = models.BooleanField(default=True)
    trust_network_infrastructure       = models.BooleanField(default=True)
    trust_news_media                   = models.BooleanField(default=True)
    trust_nudity_pornography           = models.BooleanField(default=False)
    trust_p2p_file_sharing             = models.BooleanField(default=False)
    trust_photo_sharing                = models.BooleanField(default=False)
    trust_politics                     = models.BooleanField(default=True)
    trust_portals                      = models.BooleanField(default=False)
    trust_proxy_anonymizer             = models.BooleanField(default=False)
    trust_real_estate_home_interior    = models.BooleanField(default=True)
    trust_religious                    = models.BooleanField(default=True)
    trust_search_engines               = models.BooleanField(default=False)
    trust_social_networking            = models.BooleanField(default=True)
    trust_software_technology_hardware = models.BooleanField(default=True)
    trust_sports                       = models.BooleanField(default=True)
    trust_television                   = models.BooleanField(default=True)
    trust_travel                       = models.BooleanField(default=True)
    trust_user_tracking                = models.BooleanField(default=False)
    trust_video_sharing                = models.BooleanField(default=False)
    trust_weapons                      = models.BooleanField(default=False)
    trust_webmail                      = models.BooleanField(default=True)


    def categories_as_array(self):

        array = []
        for name in BuildInCategories.CATEGORY_NAMES:

            attrname = "trust_%s" % name
            assigned = getattr(self, attrname)
            
            if assigned:
                array.append(name)

        return array

    def categories_str(self):

        values = self.categories_as_array()
        return ", ".join(values)


class RecategorizedDomain(models.Model):

    name                                = models.CharField(max_length=256, db_index=True, unique=True) # UNIQUE NOT NULL COLLATE NOCASE    

    assign_adult_themes_sexuality       = models.BooleanField(default=False)
    assign_advertising                  = models.BooleanField(default=False)
    assign_alcohol_tobacco              = models.BooleanField(default=False)
    assign_anime_manga_webcomic         = models.BooleanField(default=False)
    assign_arts_society_culture         = models.BooleanField(default=False)
    assign_automotive                   = models.BooleanField(default=False)
    assign_banking_insurance_finance    = models.BooleanField(default=False)
    assign_blogs_personal               = models.BooleanField(default=False)
    assign_business_services_industry   = models.BooleanField(default=False)
    assign_classifieds_auctions         = models.BooleanField(default=False)
    assign_content_delivery_networks    = models.BooleanField(default=False)
    assign_cracks_hacking_illegal       = models.BooleanField(default=False)
    assign_dating                       = models.BooleanField(default=False)
    assign_drugs                        = models.BooleanField(default=False)
    assign_ecommerce_shopping           = models.BooleanField(default=False)
    assign_education_science_research   = models.BooleanField(default=False)
    assign_entertainment_humor_hobby    = models.BooleanField(default=False)
    assign_expired_parked               = models.BooleanField(default=False)
    assign_fashion_beauty_cosmetics     = models.BooleanField(default=False)
    assign_file_storage                 = models.BooleanField(default=False)
    assign_food_dining_restaurants      = models.BooleanField(default=False)
    assign_forums_message_boards        = models.BooleanField(default=False)
    assign_gambling                     = models.BooleanField(default=False)
    assign_games                        = models.BooleanField(default=False)
    assign_generic_non_categorized      = models.BooleanField(default=False)
    assign_government                   = models.BooleanField(default=False)
    assign_hate_discrimination_violence = models.BooleanField(default=False)
    assign_health_medicine_fitness      = models.BooleanField(default=False)
    assign_jobs_employment_career       = models.BooleanField(default=False)
    assign_messaging_chat               = models.BooleanField(default=False)
    assign_movies                       = models.BooleanField(default=False)
    assign_music_radio                  = models.BooleanField(default=False)
    assign_network_infrastructure       = models.BooleanField(default=False)
    assign_news_media                   = models.BooleanField(default=False)
    assign_nudity_pornography           = models.BooleanField(default=False)
    assign_p2p_file_sharing             = models.BooleanField(default=False)
    assign_photo_sharing                = models.BooleanField(default=False)
    assign_politics                     = models.BooleanField(default=False)
    assign_portals                      = models.BooleanField(default=False)
    assign_proxy_anonymizer             = models.BooleanField(default=False)
    assign_real_estate_home_interior    = models.BooleanField(default=False)
    assign_religious                    = models.BooleanField(default=False)
    assign_search_engines               = models.BooleanField(default=False)
    assign_social_networking            = models.BooleanField(default=False)
    assign_software_technology_hardware = models.BooleanField(default=False)
    assign_sports                       = models.BooleanField(default=False)
    assign_television                   = models.BooleanField(default=False)
    assign_travel                       = models.BooleanField(default=False)
    assign_user_tracking                = models.BooleanField(default=False)
    assign_video_sharing                = models.BooleanField(default=False)
    assign_weapons                      = models.BooleanField(default=False)
    assign_webmail                      = models.BooleanField(default=False)


    def __unicode__(self):
        return self.name

    def categories_as_array(self):

        array = []
        for name in BuildInCategories.CATEGORY_NAMES:

            attrname = "assign_%s" % name
            assigned = getattr(self, attrname)
            
            if assigned:
                array.append(name)

        return array

    def categories_str(self):

        values = self.categories_as_array()
        return ", ".join(values)

#
#
#
class FileType(models.Model):
    name = models.CharField(max_length=254, primary_key=True, unique=True)

#
#
#
class PhraseEngine(models.Model):

    PHRASE_ENGINE_COUNT_MULTIPLE = 0
    PHRASE_ENGINE_COUNT_ONCE     = 1
    PHRASE_ENGINE_COUNT_CHOICES = (
        (PHRASE_ENGINE_COUNT_MULTIPLE, "Count all phrase occurance in text"),
        (PHRASE_ENGINE_COUNT_ONCE,     "Count phrase occurance only once in text")
    )
    count_type = models.IntegerField(default=PHRASE_ENGINE_COUNT_MULTIPLE,choices=PHRASE_ENGINE_COUNT_CHOICES)

#
#
#
class Policy(models.Model):

    name     = models.CharField(max_length=254, unique=True)
    priority = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

    #
    # block page bypass settings of a policy
    #
    
    # type of bypass
    bypass_allowed        = models.BooleanField(default=False)  # enable of disable bypass
    bypass_strip_www      = models.BooleanField(default=True)   # www.example.lan is bypassed if we bypass example.lan and vice versa
    bypass_children       = models.BooleanField(default=True)   # cdn.example.lan is bypassed if we bypass example.lan
    bypass_category       = models.BooleanField(default=False)  # not implemented
    bypass_all            = models.BooleanField(default=False)  # not implemented
    bypass_referers       = models.BooleanField(default=False)  # all URLs that have example.lan in referer are also bypassed
    bypass_duration       = models.IntegerField(default=60)     # by default each 60 minutes you will see the click_to_bypass screen
    bypass_token_required = models.BooleanField(default=False)  # bypass is ONLY allowed with the token

    # list of modules that can be bypassed (same as in exclusions) by default - everything is bypassed
    bypass_adult          = models.BooleanField(default=True)
    bypass_categories     = models.BooleanField(default=True)
    bypass_file           = models.BooleanField(default=True)
    bypass_adblock        = models.BooleanField(default=True)
    bypass_privacy        = models.BooleanField(default=True)
    bypass_http           = models.BooleanField(default=True)


#
# token list (global, not related to the policy) - ideally this needs to be the User model!
#
class ByPassToken(models.Model):

    class Meta:
        ordering = ["name"]

    value   = models.CharField(max_length=254, db_index=True, unique=True)    # token thats need to be typed into bypass popup (unique)
    name    = models.CharField(max_length=254, db_index=True)                 # name of the user who is allowed to bypass (visible in reports only)    
    comment = models.TextField(blank=True)


#
# schedule (like in Squid acl)
#
class Schedule(models.Model):

    policy = models.ForeignKey(Policy)

    # schedule - days
    on_mon = models.BooleanField(default=True)
    on_tue = models.BooleanField(default=True)
    on_wed = models.BooleanField(default=True)
    on_thu = models.BooleanField(default=True)
    on_fri = models.BooleanField(default=True)
    on_sat = models.BooleanField(default=True)
    on_sun = models.BooleanField(default=True)

    # schedule - from 00:00 to 23:59
    from_hours = models.IntegerField(default=0)
    from_mins  = models.IntegerField(default=0)
    to_hours   = models.IntegerField(default=23)
    to_mins    = models.IntegerField(default=59)

#
#
#
class Advanced(models.Model):

    policy               = models.OneToOneField(Policy, primary_key=True)
    comment              = models.TextField()
    enable               = models.BooleanField(default=True)
    sslbump              = models.BooleanField(default=True)    
    exclude_by_referer   = models.BooleanField(default=False)
    ignore_case          = models.BooleanField(default=True)
    hide_history         = models.BooleanField(default=False)
    hide_result_info     = models.BooleanField(default=True)   # if True - explicit results of what has triggered block are hidden on the blocked page
    tunnel_block         = models.BooleanField(default=True)    # True - postpone blocking after CONNECT; False - block CONNECTs right away

    def __unicode__(self):
        return "Advanced for Policy %s" % self.policy




#
#
#
class Member(models.Model):
    class Meta:
        abstract  = True
        unique_together = (("policy", "value"),)
        ordering = ["value"]

    policy  = models.ForeignKey(Policy)
    value   = models.CharField(max_length=254)
    comment = models.TextField()

    def __unicode__(self):
        return self.value

class MemberName(Member):
    pass
class MemberIp(Member):
    pass
class MemberRange(Member):
    pass
class MemberSubnet(Member):
    pass

#
#
#
class MemberLdap(models.Model):
    class Meta:
        unique_together = (("policy", "dn"),)
        ordering = ["name"]

    policy    = models.ForeignKey(Policy)
    name      = models.CharField(max_length=254)
    dn        = models.CharField(max_length=4096)
    recursive = models.BooleanField(default=False)
    comment   = models.TextField(blank=True)

#
#
#
class Exclusion(models.Model):

    class Meta:
        abstract  = True
        unique_together = (("policy", "value"),)
        ordering = ["value"]

    policy          = models.ForeignKey(Policy)
    value           = models.CharField(max_length=254)
    scan_adult      = models.BooleanField(default=False)
    scan_categories = models.BooleanField(default=False)
    scan_file       = models.BooleanField(default=False)
    scan_adblock    = models.BooleanField(default=False)
    scan_privacy    = models.BooleanField(default=False)
    scan_http       = models.BooleanField(default=False)
    comment         = models.TextField()

class ExclusionDomain(Exclusion):
    pass
class ExclusionIp(Exclusion):
    pass
class ExclusionRange(Exclusion):
    pass
class ExclusionSubnet(Exclusion):
    pass
class ExclusionUrl(Exclusion):
    pass
class ExclusionContentType(Exclusion):
    pass

#
#
#
class RuleAnnoyances(models.Model):
    policy                   = models.OneToOneField(Policy, primary_key=True)
    block_ads                = models.BooleanField(default=True)
    protect_privacy          = models.BooleanField(default=False)

#
#
#
class RuleAdult(models.Model):

    policy                   = models.OneToOneField(Policy, primary_key=True)
    trust_allowed_categories = models.BooleanField(default=True)
    enable_heuristics        = models.BooleanField(default=False)
    heuristics_maximum_weight= models.IntegerField(default=40)
    enable_image_filtering   = models.BooleanField(default=False)

    # phrases
    enable_phrases           = models.BooleanField(default=True)
    phrases_maximum_weight   = models.IntegerField(default=80)
    phrases_maximum_size     = models.IntegerField(default=2097152) # 2MB - oh YouTube!
    phrases_scan_links       = models.BooleanField(default=True)
    phrases_scan_javascript  = models.BooleanField(default=False)
    phrases_scan_css         = models.BooleanField(default=False)
    phrases_parse_links      = models.BooleanField(default=False)
        
#
#
#
class RuleApps(models.Model):

    YOUTUBE_RESTRICT_NONE     = 0
    YOUTUBE_RESTRICT_MODERATE = 1
    YOUTUBE_RESTRICT_STRICT   = 2
    YOUTUBE_RESTRICT_CHOICES  = (
        (YOUTUBE_RESTRICT_NONE, "no restrictions"),
        (YOUTUBE_RESTRICT_MODERATE, "moderate restrictions"),
        (YOUTUBE_RESTRICT_STRICT, "strict restrictions")
    )

    policy                    = models.OneToOneField(Policy, primary_key=True)
    youtube_restrictions      = models.IntegerField(choices=YOUTUBE_RESTRICT_CHOICES,default=YOUTUBE_RESTRICT_MODERATE)
    hide_yt_comments          = models.BooleanField(default=False)
    hide_yt_suggestions       = models.BooleanField(default=False)
    hide_yt_other             = models.BooleanField(default=False)
    enable_google_apps        = models.BooleanField(default=False)
    enable_safe_search        = models.BooleanField(default=True)

#
#
#
class RuleCategoryCustom(models.Model):

    class Meta:
        unique_together = ('policy', 'category')

    policy   = models.ForeignKey(Policy)
    category = models.CharField(max_length=254)         # we cannot use foregn key to custom categories as they are rebuilt every time
    enable   = models.BooleanField(default=False)       # should we block the category or not

class RuleCategory(models.Model):

    policy                             = models.OneToOneField(Policy, primary_key=True)
    block_noncategorized_domains       = models.BooleanField(default=False)  # complete block all non categorized (unknown) domains; used to create safe
                                                                             # browsing environments where only site the expert looked at are allowed

    block_adult_themes_sexuality       = models.BooleanField(default=False)
    block_advertising                  = models.BooleanField(default=False)
    block_alcohol_tobacco              = models.BooleanField(default=False)
    block_anime_manga_webcomic         = models.BooleanField(default=False)
    block_arts_society_culture         = models.BooleanField(default=False)
    block_automotive                   = models.BooleanField(default=False)
    block_banking_insurance_finance    = models.BooleanField(default=False)
    block_blogs_personal               = models.BooleanField(default=False)
    block_business_services_industry   = models.BooleanField(default=False)
    block_classifieds_auctions         = models.BooleanField(default=False)
    block_content_delivery_networks    = models.BooleanField(default=False)
    block_cracks_hacking_illegal       = models.BooleanField(default=True)
    block_dating                       = models.BooleanField(default=False)
    block_drugs                        = models.BooleanField(default=False)
    block_ecommerce_shopping           = models.BooleanField(default=False)
    block_education_science_research   = models.BooleanField(default=False)
    block_entertainment_humor_hobby    = models.BooleanField(default=False)
    block_expired_parked               = models.BooleanField(default=False)
    block_fashion_beauty_cosmetics     = models.BooleanField(default=False)
    block_file_storage                 = models.BooleanField(default=False)
    block_food_dining_restaurants      = models.BooleanField(default=False)
    block_forums_message_boards        = models.BooleanField(default=False)
    block_gambling                     = models.BooleanField(default=False)
    block_games                        = models.BooleanField(default=False)
    block_generic_non_categorized      = models.BooleanField(default=False)
    block_government                   = models.BooleanField(default=False)
    block_hate_discrimination_violence = models.BooleanField(default=False)
    block_health_medicine_fitness      = models.BooleanField(default=False)
    block_jobs_employment_career       = models.BooleanField(default=False)
    block_messaging_chat               = models.BooleanField(default=False)
    block_movies                       = models.BooleanField(default=False)
    block_music_radio                  = models.BooleanField(default=False)
    block_network_infrastructure       = models.BooleanField(default=False)
    block_news_media                   = models.BooleanField(default=False)
    block_nudity_pornography           = models.BooleanField(default=True)
    block_p2p_file_sharing             = models.BooleanField(default=False)
    block_photo_sharing                = models.BooleanField(default=False)
    block_politics                     = models.BooleanField(default=False)
    block_portals                      = models.BooleanField(default=False)
    block_proxy_anonymizer             = models.BooleanField(default=True)
    block_real_estate_home_interior    = models.BooleanField(default=False)
    block_religious                    = models.BooleanField(default=False)
    block_search_engines               = models.BooleanField(default=False)
    block_social_networking            = models.BooleanField(default=False)
    block_software_technology_hardware = models.BooleanField(default=False)
    block_sports                       = models.BooleanField(default=False)
    block_television                   = models.BooleanField(default=False)
    block_travel                       = models.BooleanField(default=False)
    block_user_tracking                = models.BooleanField(default=False)
    block_video_sharing                = models.BooleanField(default=False)
    block_weapons                      = models.BooleanField(default=False)
    block_webmail                      = models.BooleanField(default=False)

    def categories_as_array(self):

        array = []
        for name in BuildInCategories.CATEGORY_NAMES:

            attrname = "block_%s" % name
            assigned = getattr(self, attrname)
            
            if assigned:
                array.append(name)

        return array

    def categories_str(self):

        values = self.categories_as_array()
        return ", ".join(values)

#
#
#
class RuleDynamicCategory(models.Model):

    policy           = models.OneToOneField(Policy, primary_key=True)
    enabled          = models.BooleanField(default=False)
    analyze_request  = models.BooleanField(default=True)
    analyze_response = models.BooleanField(default=True)

    CLASSIFY_ONLY_UNKNOWN_SITES    = 0
    CLASSIFY_UNKNOWN_AND_UNTRUSTED = 1
    CLASSIFY_ALL_SITES             = 2
    CLASSIFY_CHOICES  = (
        (CLASSIFY_ONLY_UNKNOWN_SITES, "only unknown sites"),
        (CLASSIFY_UNKNOWN_AND_UNTRUSTED, "unknown and untrusted sites"),
        (CLASSIFY_ALL_SITES, "all sites")
    )

    classify_type = models.IntegerField(choices=CLASSIFY_CHOICES,default=CLASSIFY_UNKNOWN_AND_UNTRUSTED)

    # we have all the categories here in the model but actually we have much less classifiers 
    classify_adult_themes_sexuality       = models.BooleanField(default=True)
    classify_advertising                  = models.BooleanField(default=False)
    classify_alcohol_tobacco              = models.BooleanField(default=False)
    classify_anime_manga_webcomic         = models.BooleanField(default=False)
    classify_arts_society_culture         = models.BooleanField(default=False)
    classify_automotive                   = models.BooleanField(default=False)
    classify_banking_insurance_finance    = models.BooleanField(default=False)
    classify_blogs_personal               = models.BooleanField(default=False)
    classify_business_services_industry   = models.BooleanField(default=False)
    classify_classifieds_auctions         = models.BooleanField(default=False)
    classify_content_delivery_networks    = models.BooleanField(default=False)
    classify_cracks_hacking_illegal       = models.BooleanField(default=False)
    classify_dating                       = models.BooleanField(default=False)
    classify_drugs                        = models.BooleanField(default=True)
    classify_ecommerce_shopping           = models.BooleanField(default=False)
    classify_education_science_research   = models.BooleanField(default=False)
    classify_entertainment_humor_hobby    = models.BooleanField(default=False)
    classify_expired_parked               = models.BooleanField(default=False)
    classify_fashion_beauty_cosmetics     = models.BooleanField(default=False)
    classify_file_storage                 = models.BooleanField(default=False)
    classify_food_dining_restaurants      = models.BooleanField(default=False)
    classify_forums_message_boards        = models.BooleanField(default=False)
    classify_gambling                     = models.BooleanField(default=True)
    classify_games                        = models.BooleanField(default=False)
    classify_generic_non_categorized      = models.BooleanField(default=False)
    classify_government                   = models.BooleanField(default=False)
    classify_hate_discrimination_violence = models.BooleanField(default=False)
    classify_health_medicine_fitness      = models.BooleanField(default=False)
    classify_jobs_employment_career       = models.BooleanField(default=False)
    classify_messaging_chat               = models.BooleanField(default=False)
    classify_movies                       = models.BooleanField(default=False)
    classify_music_radio                  = models.BooleanField(default=False)
    classify_network_infrastructure       = models.BooleanField(default=False)
    classify_news_media                   = models.BooleanField(default=False)
    classify_nudity_pornography           = models.BooleanField(default=True)
    classify_p2p_file_sharing             = models.BooleanField(default=False)
    classify_photo_sharing                = models.BooleanField(default=False)
    classify_politics                     = models.BooleanField(default=False)
    classify_portals                      = models.BooleanField(default=False)
    classify_proxy_anonymizer             = models.BooleanField(default=False)
    classify_real_estate_home_interior    = models.BooleanField(default=False)
    classify_religious                    = models.BooleanField(default=False)
    classify_search_engines               = models.BooleanField(default=False)
    classify_social_networking            = models.BooleanField(default=False)
    classify_software_technology_hardware = models.BooleanField(default=False)
    classify_sports                       = models.BooleanField(default=False)
    classify_television                   = models.BooleanField(default=False)
    classify_travel                       = models.BooleanField(default=False)
    classify_user_tracking                = models.BooleanField(default=False)
    classify_video_sharing                = models.BooleanField(default=False)
    classify_weapons                      = models.BooleanField(default=False)
    classify_webmail                      = models.BooleanField(default=False)

    def categories_as_array(self):

        array = []
        for name in BuildInCategories.CATEGORY_NAMES:

            attrname = "classify_%s" % name
            assigned = getattr(self, attrname)
            
            if assigned:
                array.append(name)

        return array

    def categories_str(self):

        values = self.categories_as_array()
        return ", ".join(values)

    

#
#
#
class RuleValue(models.Model):

    class Meta:
        abstract = True
        unique_together = ('policy', 'value')

    policy  = models.ForeignKey(Policy)
    value   = models.CharField(max_length=254)
    comment = models.TextField()

class RuleDomain(RuleValue):
    pass
class RuleUrl(RuleValue):
    pass
class RuleUserAgent(RuleValue):
    pass
class RuleContentType(RuleValue):
    pass
class RuleCharset(RuleValue):
    pass
class RuleFileName(RuleValue):
    pass
class RuleFileContent(RuleValue):
    pass

class RuleFileSize(models.Model):
    policy   = models.OneToOneField(Policy, primary_key=True)
    enable   = models.BooleanField(default=False)
    max_size = models.IntegerField(default=1048576) # 1MB

#
# Clustering
#

class ClusteringClient(models.Model):

    enabled          = models.BooleanField(default=False)
    sync_interval    = models.IntegerField(default=5)   
    port             = models.IntegerField(default=18999)  
    server_address   = models.CharField(max_length=254)
    cert_file        = models.CharField(max_length=254)
    private_key_file = models.CharField(max_length=254)
    ca_file          = models.CharField(max_length=254)


class ClusteringServer(models.Model):

    enabled          = models.BooleanField(default=False)
    server_address   = models.CharField(max_length=254)
    port             = models.IntegerField(default=18999) 
    cert_file        = models.CharField(max_length=254)
    private_key_file = models.CharField(max_length=254)
    ca_file          = models.CharField(max_length=254)
