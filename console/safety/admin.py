#
# django
#
from django.contrib import admin

#
# ours
#
from safety.models import *

#
# some useful mixins
#
class NoDeleteMixin:
    def has_delete_permission(self, request, obj=None):
        return False
        
class NoAddMixin:
    def has_add_permission(self, request, obj=None):
        return False
        
class NoEditMixin:
    def has_change_permission(self, request, obj=None):
        return False

#
#
#
admin.site.register(Safety)
admin.site.register(Network)
admin.site.register(Annoyances)

#
#
#
class AppsAdmin(NoDeleteMixin, NoAddMixin, admin.ModelAdmin):    
    pass
admin.site.register(Apps, AppsAdmin)

#
#
#
class EmptyAdmin(NoDeleteMixin, NoAddMixin, NoEditMixin, admin.ModelAdmin):    
    list_display = ('name', )
    
admin.site.register(FileType, EmptyAdmin)
admin.site.register(CustomCategory, EmptyAdmin)
admin.site.register(RecategorizedDomain)


admin.site.register(PhraseEngine)

class PolicyAdmin(admin.ModelAdmin):    
    list_display = ('name', 'priority')

admin.site.register(Policy, PolicyAdmin)
admin.site.register(Schedule)

class AdvancedAdmin(NoDeleteMixin, NoAddMixin, admin.ModelAdmin):    
    list_display = ('policy', 'enable', 'exclude_by_referer', 'ignore_case', 'hide_history')
    
admin.site.register(Advanced, AdvancedAdmin)

#
#
#
class MemberAdmin(admin.ModelAdmin):
    list_filter  = ['policy']
    list_display = ('value', 'policy')

admin.site.register(MemberName, MemberAdmin)
admin.site.register(MemberIp, MemberAdmin)
admin.site.register(MemberRange, MemberAdmin)
admin.site.register(MemberSubnet, MemberAdmin)

#
#
#
class MemberLdapAdmin(admin.ModelAdmin):
    list_filter  = ['policy']
    list_display = ('name', 'dn', 'recursive', 'policy')
    
admin.site.register(MemberLdap, MemberLdapAdmin)

#
#
#
class ExclusionAdmin(admin.ModelAdmin):
    list_filter  = ['policy']
    list_display = ('value', 'policy', 'scan_adult', 'scan_categories', 'scan_file', 'scan_adblock', 'scan_privacy', 'scan_http')
    
admin.site.register(ExclusionDomain, ExclusionAdmin)
admin.site.register(ExclusionIp, ExclusionAdmin)
admin.site.register(ExclusionRange, ExclusionAdmin)
admin.site.register(ExclusionSubnet, ExclusionAdmin)
admin.site.register(ExclusionUrl, ExclusionAdmin)
admin.site.register(ExclusionContentType, ExclusionAdmin)

#
#
#
class RuleAnnoyancesAdmin(admin.ModelAdmin):
    list_filter   = ['policy']
    list_display  = ('policy', 'block_ads', 'protect_privacy')
admin.site.register(RuleAnnoyances, RuleAnnoyancesAdmin)

#
#
#
class RuleAdultAdmin(admin.ModelAdmin):
    list_filter   = ['policy']
    list_display  = ('policy', 'enable_heuristics', 'enable_image_filtering', 'enable_phrases')

admin.site.register(RuleAdult, RuleAdultAdmin)

#
#
#
class RuleAppsAdmin(admin.ModelAdmin):
    list_filter   = ['policy']
    list_display  = ('policy', 'youtube_restrictions', 'enable_google_apps', 'enable_safe_search')    
admin.site.register(RuleApps, RuleAppsAdmin)


admin.site.register(RuleCategory)
admin.site.register(RuleCategoryCustom)

class RuleValueAdmin(admin.ModelAdmin):
    list_filter   = ['policy']
    list_display  = ('value', 'policy', 'comment')

admin.site.register(RuleDomain, RuleValueAdmin)
admin.site.register(RuleUrl, RuleValueAdmin)
admin.site.register(RuleContentType, RuleValueAdmin)
admin.site.register(RuleCharset, RuleValueAdmin)
admin.site.register(RuleFileName)
admin.site.register(RuleFileContent)

admin.site.register(ClusteringClient)
admin.site.register(ClusteringServer)
