#
#
#
import urlparse
import datetime
import itertools

#
#
#
from utility.tldextract import *

#
# describes a surfing record
#   
class SurfingRecord:

    def __init__(self, fields='None'):
        if fields == 'None':
            return

        (o, d, t, h) = self.parse_timestamp(int(fields['timestamp']))

        self.server       = fields['server']                                 # string
        self.timestamp    = o                                                # string original timestamp in UTC
        self.date         = d                                                # string date from timestamp
        self.time         = t                                                # string time from timestamp
        self.hour         = h                                                # string hour 0-23 from timestamp
        self.iid          = int(fields['iid'])                               # int
        self.duration     = fields['duration']                               # int
        self.timing       = int(fields['timing'])                            # int
        self.size         = int(fields['size'])                              # int
        self.size_approx  = 0                                                # int - and in was not in 4.1 to so make it more
        if 'size_approx' in fields:                                          #       robust we set the default to 0
            self.size_approx = int(fields['size_approx'])                    
        self.flags        = self.parse_flags(fields['flags'])                # array
        self.categories   = self.parse_categories(int(fields['categories'])) # array
        self.trusted      = int(fields['trusted'])
        self.message      = self.parse_message(fields['message'])            # icap::request_type (string)
        self.user_ip      = fields['user_ip']
        self.user_name    = fields['user_name']                              # string
        
        self.user_agent   = ""
        if 'user_agent' in fields:                                           
            self.user_agent = fields['user_agent']                  
                           
        self.policy       = fields['policy']                                 # string
        self.content_type = self.parse_content_type(fields['content_type'])  # string
        self.module       = self.parse_module(fields['module'])              # ql::br::module_type (string)
        self.level        = self.parse_level(fields['level'])                # icap::scan_level (string)
        self.verdict      = self.parse_verdict(fields['verdict'])            # icap::scan_verdict (string)        
        self.offensive    = self.parse_offensive(self.verdict, self.module)
        self.unproductive = self.parse_unproductive(self.categories)
        self.param1       = fields['param1']                                 # string
        self.param2       = fields['param2']                                 # string
        self.mtime        = fields['mtime']                                  # int
        self.host         = fields['host']                                   # string
        self.tld          = self.get_tld(fields['url'])
        self.url          = fields['url']                                    # string
        self.method       = self.parse_method(fields['method'])              # ql::br::method_type (string)
        
        if fields['method'] == 'CONNECT':
            url  = urlparse.urlparse(fields['url'])            
            self.scheme = "connect"                                     # string
            self.path   = url.path                                      # string            
            self.query  = ""
        else:            
            url  = urlparse.urlparse(fields['url'])
            self.scheme = url.scheme                                    # string
            self.path   = url.path                                      # string
            self.query  = url.query                                     # string
        
        # parse referer
        if len(fields['referer']) > 0:
            ref_url         = urlparse.urlparse(fields['referer'])
            self.ref_scheme = ref_url.scheme
            self.ref_host   = ref_url.netloc
            self.ref_path   = ref_url.path
            
    def get_tld(self, url):
        ext = tldextract.extract(url)
        return ext.domain + "." + ext.suffix 
            
    def parse_timestamp(self, timestamp):
        # the input timestamp here is in UTC        
        v = datetime.datetime.fromtimestamp(timestamp)
        o = v.strftime("%Y-%m-%d %H:%M:%S")
        d = v.strftime("%Y-%m-%d")
        t = v.strftime("%H:%M:%S")
        h = v.strftime("%H")
        return (o, d, t, h)
            
    def parse_method(self, method):
        method_unknown = 0 
        method_get     = 1 
        method_post    = 2 
        method_head    = 3 
        method_delete  = 4 
        method_options = 5
        method_put     = 6
        method_trace   = 7
        method_connect = 8
        
        if method == method_get:
            return "GET"
        if method == method_post:
            return "POST"        
        if method == method_head:
            return "HEAD"        
        if method == method_delete:
            return "DELETE"        
        if method == method_options:
            return "OPTIONS"        
        if method == method_put:
            return "PUT"        
        if method == method_trace:        
            return "TRACE"        
        if method == method_connect:
            return "CONNECT"        
        return "UNKNOWN"
        
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
        
    def is_whitelisted(self):
        flags = self.flags
        for key in flags.keys():
            if flags[key]:
                return False
        return True # the record was whitelisted when all scan flags are False
        
        
    def get_flags_as_string(self):
        
        array = []
        flags = self.flags
        
        for key in flags.keys():
            str = key
            if flags[key]:
                str += "+"
            else:
                str += "-"
            array.append(str)
            
        return ", ".join(array)
        
    def parse_categories(self, categories):
    
        # these are bits for categories
        CATEGORY_NONE                         = 0
        CATEGORY_ADULT_THEMES_SEXUALITY       = 1 << 1
        CATEGORY_ADVERTISING                  = 1 << 2
        CATEGORY_ALCOHOL_TOBACCO              = 1 << 3
        CATEGORY_ANIME_MANGA_WEBCOMIC         = 1 << 4
        CATEGORY_ARTS_SOCIETY_CULTURE         = 1 << 5
        CATEGORY_AUTOMOTIVE                   = 1 << 6
        CATEGORY_BANKING_INSURANCE_FINANCE    = 1 << 7
        CATEGORY_BLOGS_PERSONAL               = 1 << 8
        CATEGORY_BUSINESS_SERVICES_INDUSTRY   = 1 << 9
        CATEGORY_CLASSIFIEDS_AUCTIONS         = 1 << 10
        CATEGORY_CONTENT_DELIVERY_NETWORKS    = 1 << 11
        CATEGORY_CRACKS_HACKING_ILLEGAL       = 1 << 12
        CATEGORY_DATING                       = 1 << 13
        CATEGORY_DRUGS                        = 1 << 14
        CATEGORY_ECOMMERCE_SHOPPING           = 1 << 15
        CATEGORY_EDUCATION_SCIENCE_RESEARCH   = 1 << 16
        CATEGORY_ENTERTAINMENT_HUMOR_HOBBY    = 1 << 17
        CATEGORY_EXPIRED_PARKED               = 1 << 18
        CATEGORY_FASHION_BEAUTY_COSMETICS     = 1 << 19
        CATEGORY_FILE_STORAGE                 = 1 << 20
        CATEGORY_FOOD_DINING_RESTAURANTS      = 1 << 21
        CATEGORY_FORUMS_MESSAGE_BOARDS        = 1 << 22
        CATEGORY_GAMBLING                     = 1 << 23
        CATEGORY_GAMES                        = 1 << 24
        CATEGORY_GENERIC_NON_CATEGORIZED      = 1 << 25
        CATEGORY_GOVERNMENT                   = 1 << 26
        CATEGORY_HATE_DISCRIMINATION_VIOLENCE = 1 << 27
        CATEGORY_HEALTH_MEDICINE_FITNESS      = 1 << 28
        CATEGORY_JOBS_EMPLOYMENT_CAREER       = 1 << 29
        CATEGORY_MESSAGING_CHAT               = 1 << 30
        CATEGORY_MOVIES                       = 1 << 31
        CATEGORY_MUSIC_RADIO                  = 1 << 32
        CATEGORY_NETWORK_INFRASTRUCTURE       = 1 << 33
        CATEGORY_NEWS_MEDIA                   = 1 << 34
        CATEGORY_NUDITY_PORNOGRAPHY           = 1 << 35
        CATEGORY_P2P_FILE_SHARING             = 1 << 36
        CATEGORY_PHOTO_SHARING                = 1 << 37
        CATEGORY_POLITICS                     = 1 << 38
        CATEGORY_PORTALS                      = 1 << 39
        CATEGORY_PROXY_ANONYMIZER             = 1 << 40
        CATEGORY_REAL_ESTATE_HOME_INTERIOR    = 1 << 41
        CATEGORY_RELIGIOUS                    = 1 << 42
        CATEGORY_SEARCH_ENGINES               = 1 << 43
        CATEGORY_SOCIAL_NETWORKING            = 1 << 44
        CATEGORY_SOFTWARE_TECHNOLOGY_HARDWARE = 1 << 45
        CATEGORY_SPORTS                       = 1 << 46
        CATEGORY_TELEVISION                   = 1 << 47
        CATEGORY_TRAVEL                       = 1 << 48
        CATEGORY_USER_TRACKING                = 1 << 49
        CATEGORY_VIDEO_SHARING                = 1 << 50
        CATEGORY_WEAPONS                      = 1 << 51
        CATEGORY_WEBMAIL                      = 1 << 52
        CATEGORY_MAXIMUM                      = 1 << 53

        result = []


        if categories & CATEGORY_ADULT_THEMES_SEXUALITY:
            result.append("adult_themes_sexuality")
        
        if categories & CATEGORY_ADVERTISING:
            result.append("advertising")
        
        if categories & CATEGORY_ALCOHOL_TOBACCO:
            result.append("alcohol_tobacco")
        
        if categories & CATEGORY_ANIME_MANGA_WEBCOMIC:
            result.append("anime_manga_webcomic")
        
        if categories & CATEGORY_ARTS_SOCIETY_CULTURE:
            result.append("arts_society_culture")
        
        if categories & CATEGORY_AUTOMOTIVE:
            result.append("automotive")
        
        if categories & CATEGORY_BANKING_INSURANCE_FINANCE:
            result.append("banking_insurance_finance")
        
        if categories & CATEGORY_BLOGS_PERSONAL:
            result.append("blogs_personal")
        
        if categories & CATEGORY_BUSINESS_SERVICES_INDUSTRY:
            result.append("business_services_industry")
        
        if categories & CATEGORY_CLASSIFIEDS_AUCTIONS:
            result.append("classifieds_auctions")
        
        if categories & CATEGORY_CONTENT_DELIVERY_NETWORKS:
            result.append("content_delivery_networks")

        if categories & CATEGORY_CRACKS_HACKING_ILLEGAL:
            result.append("cracks_hacking_illegal")
        
        if categories & CATEGORY_DATING:
            result.append("dating")
        
        if categories & CATEGORY_DRUGS:
            result.append("drugs")
        
        if categories & CATEGORY_ECOMMERCE_SHOPPING:
            result.append("ecommerce_shopping")
        
        if categories & CATEGORY_EDUCATION_SCIENCE_RESEARCH:
            result.append("education_science_research")
        
        if categories & CATEGORY_ENTERTAINMENT_HUMOR_HOBBY:
            result.append("entertainment_humor_hobby")

        if categories & CATEGORY_EXPIRED_PARKED:
            result.append("expired_parked")
        
        if categories & CATEGORY_FASHION_BEAUTY_COSMETICS:
            result.append("fashion_beauty_cosmetics")
        
        if categories & CATEGORY_FILE_STORAGE:
            result.append("file_storage")
        
        if categories & CATEGORY_FOOD_DINING_RESTAURANTS:
            result.append("food_dining_restaurants")
        
        if categories & CATEGORY_FORUMS_MESSAGE_BOARDS:
            result.append("forums_message_boards")
        
        if categories & CATEGORY_GAMBLING:
            result.append("gambling")
        
        if categories & CATEGORY_GAMES:
            result.append("games")

        if categories & CATEGORY_GENERIC_NON_CATEGORIZED:
            result.append("generic_non_categorized")
        
        if categories & CATEGORY_GOVERNMENT:
            result.append("government")
        
        if categories & CATEGORY_HATE_DISCRIMINATION_VIOLENCE:
            result.append("hate_discrimination_violence")
        
        if categories & CATEGORY_HEALTH_MEDICINE_FITNESS:
            result.append("health_medicine_fitness")
        
        if categories & CATEGORY_JOBS_EMPLOYMENT_CAREER:
            result.append("jobs_employment_career")
        
        if categories & CATEGORY_MESSAGING_CHAT:
            result.append("messaging_chat")
        
        if categories & CATEGORY_MOVIES:
            result.append("movies")
        
        if categories & CATEGORY_MUSIC_RADIO:
            result.append("music_radio")
        
        if categories & CATEGORY_NETWORK_INFRASTRUCTURE:
            result.append("network_infrastructure")
        
        if categories & CATEGORY_NEWS_MEDIA:
            result.append("news_media")
        
        if categories & CATEGORY_NUDITY_PORNOGRAPHY:
            result.append("nudity_pornography")
        
        if categories & CATEGORY_P2P_FILE_SHARING:
            result.append("p2p_file_sharing")
        
        if categories & CATEGORY_PHOTO_SHARING:
            result.append("photo_sharing")
        
        if categories & CATEGORY_POLITICS:
            result.append("politics")
        
        if categories & CATEGORY_PORTALS:
            result.append("portals")
        
        if categories & CATEGORY_PROXY_ANONYMIZER:
            result.append("proxy_anonymizer")
        
        if categories & CATEGORY_REAL_ESTATE_HOME_INTERIOR:
            result.append("real_estate_home_interior")
        
        if categories & CATEGORY_RELIGIOUS:
            result.append("religious")
        
        if categories & CATEGORY_SEARCH_ENGINES:
            result.append("search_engines")
        
        if categories & CATEGORY_SOCIAL_NETWORKING:
            result.append("social_networking")
        
        if categories & CATEGORY_SOFTWARE_TECHNOLOGY_HARDWARE:
            result.append("software_technology_hardware")
        
        if categories & CATEGORY_SPORTS:
            result.append("sports")
        
        if categories & CATEGORY_TELEVISION:
            result.append("television")
        
        if categories & CATEGORY_TRAVEL:
            result.append("travel")

        if categories & CATEGORY_USER_TRACKING:
            result.append("user_tracking")
        
        if categories & CATEGORY_VIDEO_SHARING:
            result.append("video_sharing")
        
        if categories & CATEGORY_WEAPONS:
            result.append("weapons")
        
        if categories & CATEGORY_WEBMAIL:
            result.append("webmail")
            
        return result
        
    def get_categories_as_string(self):
        return ", ".join(self.categories)
        
    def parse_content_type(self, value):
        pos = value.find(";")
        if pos == -1:
            return value
        return value[:pos]
        
    def parse_module(self, module):
        
        module_type_clean                           = 1 << 1
        module_type_adblock                         = 1 << 2
        module_type_privacy                         = 1 << 3
        module_type_adult_heuristics                = 1 << 4
        module_type_adult_notused1                  = 1 << 5
        module_type_adult_safesearch                = 1 << 6
        module_type_adult_youtube                   = 1 << 7
        module_type_adult_phrases                   = 1 << 8
        module_type_adult_image                     = 1 << 9        
        module_type_categories                      = 1 << 10
        module_type_custom                          = 1 << 11
        module_type_http_sanitation                 = 1 << 12
        module_type_content_content_type            = 1 << 13
        module_type_content_charset                 = 1 << 14
        module_type_content_transfer_encoding       = 1 << 15
        module_type_content_file_name               = 1 << 16
        module_type_content_file_type               = 1 << 17
        module_type_content_file_size               = 1 << 18
        module_type_apps                            = 1 << 19
        module_type_sslbump                         = 1 << 20
        
        if module == module_type_clean:
            return "clean"
        if module == module_type_adblock:
            return "adblock"
        if module == module_type_privacy:
            return "privacy"
        if module == module_type_adult_heuristics:
            return "adult_heuristics"
        if module == module_type_adult_notused1:
            return "notused1"
        if module == module_type_adult_safesearch:
            return "safe_search"
        if module == module_type_adult_youtube:
            return "safe_youtube"
        if module == module_type_adult_phrases:
            return "adult_phrases"
        if module == module_type_adult_image:
            return "adult_image"
        if module == module_type_categories:
            return "categories"
        if module == module_type_custom:
            return "custom"
        if module == module_type_http_sanitation:
            return "http_sanitation"
        if module == module_type_content_content_type:
            return "content_content_type"
        if module == module_type_content_charset:
            return "content_charset"
        if module == module_type_content_transfer_encoding:
            return "content_transfer_encoding"
        if module == module_type_content_file_name:
            return "content_file_name"
        if module == module_type_content_file_type:
            return "content_file_type"
        if module == module_type_content_file_size:
            return "content_file_size"        
        if module == module_type_apps:
            return "apps"
        if module == module_type_sslbump:
            return "skip_sslbump"

        return "unknown"
        
    def parse_message(self, message):
        unknown = 0
        options = 1
        reqmod  = 2
        respmod = 3
        
        if message == options:
            return "OPTIONS"
        if message == reqmod:
            return "request"
        if message == respmod:
            return "response"
        
        return "UNKNOWN"
        
    def parse_level(self, level):
    
        processing_step_unknown      = 0
        processing_step_headers_only = 1 
        processing_step_partial_body = 2
        processing_step_limited_body = 3
        processing_step_full_body    = 4
        
        if level == processing_step_headers_only:
            return "headers"
        if level == processing_step_partial_body:
            return "partial"
        if level == processing_step_limited_body:
            return "limited"
        if level == processing_step_full_body:
            return "body"
    
        return "unknown"
        
    def parse_verdict(self, verdict):
        pass_unmodified              = 0
        pass_adapted                 = 1
        generate_artificial_response = 2
        need_more_data_for_analyzis  = 3
        
        if verdict == pass_adapted:
            return "adapt"
        if verdict == generate_artificial_response:
            return "block"
        if verdict == need_more_data_for_analyzis:
            return "rescan"
        
        return "pass"

    def parse_offensive(self, verdict, module):
        if verdict != "block":
            return False
        if module in ("adblock", "privacy"):
            return False
        return True

    def parse_unproductive(self, categories):
        for unproductive_category in [
            "adult_themes_sexuality", "alcohol_tobacco", "dating", "drugs", 
            "gambling", "games", "hate_discrimination_violence", 
            "entertainment_humor_hobby", "p2p_file_sharing", 
            "proxy_anonymizer", "nudity_pornography"
        ]:
            if unproductive_category in categories:
                return True
        return False



