#
#
#
from django.db import models

#
#
#
from _domain.safety import BuildInCategories

#
#
#
from .value import ValueModel

#
# exclusions - base model
#
class ExcludeValueModel(ValueModel):

    class Meta:        
        abstract = True
        ordering = ["value"] 
        
    bypass_adaptation = models.BooleanField(default=True)
    bypass_sslbump    = models.BooleanField(default=True)
    bypass_auth       = models.BooleanField(default=True)
    bypass_cache      = models.BooleanField(default=True)
    bypass_urlrewrite = models.BooleanField(default=True)

    def bypass_as_string(self):

    	array = []
    	if self.bypass_adaptation:
    		array.append("web filter")
    	if self.bypass_sslbump:
    		array.append("sslbump")
    	if self.bypass_auth:
    		array.append("auth")
    	if self.bypass_cache:
    		array.append("cache")
    	if self.bypass_urlrewrite:
    		array.append("safe browsing")
    	
    	if len(array) == 5 or len(array) == 0:
    		return ""

    	return ", ".join(array)




#
# exclude by remote domain attributes
#
class ExcludeDomainName(ExcludeValueModel):
    pass

class ExcludeDomainIp(ExcludeValueModel):
    pass 

class ExcludeDomainSubnet(ExcludeValueModel):
    pass

class ExcludeDomainRange(ExcludeValueModel):
    pass

#
# exclude by user attributes
#
class ExcludeUserName(ExcludeValueModel):
    pass

class ExcludeUserIp(ExcludeValueModel):
    pass

class ExcludeUserSubnet(ExcludeValueModel):
    pass

class ExcludeUserRange(ExcludeValueModel):
    pass

#
# other exclusion attributes
#
class ExcludeUserAgent(ExcludeValueModel):
    pass

class ExcludeSchedule(ExcludeValueModel):
    pass

#
# content type exclusion
#
class ExcludeContentType(ValueModel):

    class Meta:
        ordering = ["value"]

    bypass_adaptation = models.BooleanField(default=True)
    bypass_cache      = models.BooleanField(default=True)

#
# advanced exclusions acls (as-is) - note we are using TextField for value thus inheritance from ValueModel is not possible
#
class ExcludeAdvanced(models.Model):

    value_sslbump    = models.TextField(blank=True)
    value_adaptation = models.TextField(blank=True)
    value_auth       = models.TextField(blank=True)
    value_cache      = models.TextField(blank=True)
    value_urlrewrite = models.TextField(blank=True)

#
# exclude by category (for now only bypass_ssl)
#
class ExcludeCategories(models.Model):

    exclude_adult_themes_sexuality       = models.BooleanField(default=False)
    exclude_advertising                  = models.BooleanField(default=False)
    exclude_alcohol_tobacco              = models.BooleanField(default=False)
    exclude_anime_manga_webcomic         = models.BooleanField(default=False)
    exclude_arts_society_culture         = models.BooleanField(default=False)
    exclude_automotive                   = models.BooleanField(default=False)
    exclude_banking_insurance_finance    = models.BooleanField(default=True)
    exclude_blogs_personal               = models.BooleanField(default=False)
    exclude_business_services_industry   = models.BooleanField(default=False)
    exclude_classifieds_auctions         = models.BooleanField(default=False)
    exclude_content_delivery_networks    = models.BooleanField(default=False)
    exclude_cracks_hacking_illegal       = models.BooleanField(default=False)
    exclude_dating                       = models.BooleanField(default=False)
    exclude_drugs                        = models.BooleanField(default=False)
    exclude_ecommerce_shopping           = models.BooleanField(default=False)
    exclude_education_science_research   = models.BooleanField(default=False)
    exclude_entertainment_humor_hobby    = models.BooleanField(default=False)
    exclude_expired_parked               = models.BooleanField(default=False)
    exclude_fashion_beauty_cosmetics     = models.BooleanField(default=False)
    exclude_file_storage                 = models.BooleanField(default=False)
    exclude_food_dining_restaurants      = models.BooleanField(default=False)
    exclude_forums_message_boards        = models.BooleanField(default=False)
    exclude_gambling                     = models.BooleanField(default=False)
    exclude_games                        = models.BooleanField(default=False)
    exclude_generic_non_categorized      = models.BooleanField(default=False)
    exclude_government                   = models.BooleanField(default=True)
    exclude_hate_discrimination_violence = models.BooleanField(default=False)
    exclude_health_medicine_fitness      = models.BooleanField(default=True)
    exclude_jobs_employment_career       = models.BooleanField(default=False)
    exclude_messaging_chat               = models.BooleanField(default=False)
    exclude_movies                       = models.BooleanField(default=False)
    exclude_music_radio                  = models.BooleanField(default=False)
    exclude_network_infrastructure       = models.BooleanField(default=True)
    exclude_news_media                   = models.BooleanField(default=False)
    exclude_nudity_pornography           = models.BooleanField(default=False)
    exclude_p2p_file_sharing             = models.BooleanField(default=False)
    exclude_photo_sharing                = models.BooleanField(default=False)
    exclude_politics                     = models.BooleanField(default=False)
    exclude_portals                      = models.BooleanField(default=False)
    exclude_proxy_anonymizer             = models.BooleanField(default=False)
    exclude_real_estate_home_interior    = models.BooleanField(default=False)
    exclude_religious                    = models.BooleanField(default=False)
    exclude_search_engines               = models.BooleanField(default=False)
    exclude_social_networking            = models.BooleanField(default=False)
    exclude_software_technology_hardware = models.BooleanField(default=False)
    exclude_sports                       = models.BooleanField(default=False)
    exclude_television                   = models.BooleanField(default=False)
    exclude_travel                       = models.BooleanField(default=False)
    exclude_user_tracking                = models.BooleanField(default=False)
    exclude_video_sharing                = models.BooleanField(default=False)
    exclude_weapons                      = models.BooleanField(default=False)
    exclude_webmail                      = models.BooleanField(default=False)


    def categories_as_array(self):

        array = []
        for name in BuildInCategories.CATEGORY_NAMES:

            attrname = "exclude_%s" % name
            assigned = getattr(self, attrname)
            
            if assigned:
                array.append(name)

        return array

    def categories_str(self):

        values = self.categories_as_array()
        return ", ".join(values)