#
# django
#
from django.conf.urls import url

#
# ours
#
from safety import views

#
# routes
#
urlpatterns = [

    # settings
    url(r'^settings/network$', views.ViewSettingsNetwork.as_view(), name='ViewSettingsNetwork'),
    url(r'^settings/trusted/categories$', views.ViewSettingsTrustedCategories.as_view(), name='ViewSettingsTrustedCategories'),
    url(r'^recategorized/domains$', views.ViewRecategorizedDomains.as_view(), name='ViewRecategorizedDomains'),
    url(r'^recategorized/domains/create$', views.ViewRecategorizedDomainCreate.as_view(), name='ViewRecategorizedDomainCreate'),
    url(r'^recategorized/domains/(?P<pk>\d+)/update$', views.ViewRecategorizedDomainUpdate.as_view(), name='ViewRecategorizedDomainUpdate'),    
    url(r'^settings/bypass/list$', views.ViewSettingsByPass.as_view(), name='ViewSettingsByPass'),
    url(r'^settings/bypass/create$', views.ViewSettingsByPassCreate.as_view(), name='ViewSettingsByPassCreate'),
    url(r'^settings/bypass/(?P<pk>\d+)/update$', views.ViewSettingsByPassUpdate.as_view(), name='ViewSettingsByPassUpdate'),
    url(r'^settings/webapps/update$', views.ViewSettingsApps.as_view(), name='ViewSettingsApps'),

    # updates
    url(r'^subscriptions/adblock$', views.ViewSubscriptionsAdBlock.as_view(), name='ViewSubscriptionsAdBlock'),
    url(r'^subscriptions/privacy$', views.ViewSubscriptionsPrivacy.as_view(), name='ViewSubscriptionsPrivacy'),
    url(r'^subscriptions/custom$',  views.ViewCustomCategories.as_view(), name='ViewCustomCategories'),
    url(r'^subscriptions/advanced$',  views.ViewSubscriptionsAdvanced.as_view(), name='ViewSubscriptionsAdvanced'),
    

    # logs
    url(r'^support/system/info$', views.ViewSafetySystemInfo.as_view(), name='ViewSafetySystemInfo'),
    url(r'^support/update/log$', views.ViewSafetyUpdateLog.as_view(), name='ViewSafetyUpdateLog'),
    url(r'^support/error/log$', views.ViewSafetyErrorLog.as_view(), name='ViewSafetyErrorLog'),
    
    # tools    
    url(r'^tools/import/txt$', views.ViewImportTxt.as_view(), name='ViewImportTxt'),

    # policy
    url(r'^policy/$', views.PolicyList.as_view(), name='ViewPolicyList'),
    url(r'^policy/create$', views.View_PolicyCreate.as_view(), name='View_PolicyCreate'),
    url(r'^policy/(?P<pid>\d+)/copy$', views.View_PolicyCopy.as_view(), name='View_PolicyCopy'),
    url(r'^policy/(?P<pid>\d+)/priority/up/$', views.View_PolicyMoveUp.as_view(), name='View_PolicyMoveUp'),
    url(r'^policy/(?P<pk>\d+)/remove/$', views.ViewPolicyDelete.as_view(), name='ViewPolicyDelete'),    
    url(r'^policy/(?P<pk>\d+)/bypass/update$', views.ViewByPass.as_view(), name='ViewByPass'),
    url(r'^policy/(?P<pid>\d+)/advanced/update$', views.ViewAdvanced.as_view(), name='ViewAdvanced'),
    url(r'^policy/(?P<pid>\d+)/schedule$', views.ViewScheduleList.as_view(), name='ViewScheduleList'),
    url(r'^policy/(?P<pid>\d+)/schedule/create$', views.ViewScheduleCreate.as_view(), name='ViewScheduleCreate'),
    url(r'^policy/(?P<pid>\d+)/schedule/(?P<pk>\d+)/update$', views.ViewScheduleUpdate.as_view(), name='ViewScheduleUpdate'),

    # rules
    url(r'^policy/(?P<pid>\d+)/rule/adult/update$', views.ViewRuleAdult.as_view(), name='ViewRuleAdult'),
    url(r'^policy/(?P<pid>\d+)/rule/apps/update$', views.ViewRuleApps.as_view(), name='ViewRuleApps'),
    url(r'^policy/(?P<pid>\d+)/rule/annoyances/update$', views.ViewRuleAnnoyances.as_view(), name='ViewRuleAnnoyances'),
    url(r'^policy/(?P<pid>\d+)/rule/category$', views.ViewRuleCategoryBuiltIn.as_view(), name='ViewRuleCategoryBuiltIn'),
    url(r'^policy/(?P<pid>\d+)/rule/custom/$', views.ViewRuleCategoryCustom.as_view(), name='ViewRuleCategoryCustom'),
    url(r'^policy/(?P<pid>\d+)/rule/dynamic/edit/$', views.ViewRuleCategoryDynamic.as_view(), name='ViewRuleCategoryDynamic'),
    
    url(r'^policy/(?P<pid>\d+)/rule/domain/$', views.ViewRuleDomainList.as_view(), name='ViewRuleDomainList'),
    url(r'^policy/(?P<pid>\d+)/rule/domain/create$', views.ViewRuleDomainCreate.as_view(), name='ViewRuleDomainCreate'),
    url(r'^policy/(?P<pid>\d+)/rule/domain/(?P<pk>\d+)/update$', views.ViewRuleDomainUpdate.as_view(), name='ViewRuleDomainUpdate'),    
    url(r'^policy/(?P<pid>\d+)/rule/url/$', views.ViewRuleUrlList.as_view(), name='ViewRuleUrlList'),
    url(r'^policy/(?P<pid>\d+)/rule/url/create$', views.ViewRuleUrlCreate.as_view(), name='ViewRuleUrlCreate'),
    url(r'^policy/(?P<pid>\d+)/rule/url/(?P<pk>\d+)/update$', views.ViewRuleUrlUpdate.as_view(), name='ViewRuleUrlUpdate'),
    url(r'^policy/(?P<pid>\d+)/rule/user/agent/$', views.ViewRuleUserAgentList.as_view(), name='ViewRuleUserAgentList'),
    url(r'^policy/(?P<pid>\d+)/rule/user/agent/create$', views.ViewRuleUserAgentCreate.as_view(), name='ViewRuleUserAgentCreate'),
    url(r'^policy/(?P<pid>\d+)/rule/user/agent/(?P<pk>\d+)/update$', views.ViewRuleUserAgentUpdate.as_view(), name='ViewRuleUserAgentUpdate'),
    url(r'^policy/(?P<pid>\d+)/rule/charset/$', views.ViewRuleCharsetList.as_view(), name='ViewRuleCharsetList'),
    url(r'^policy/(?P<pid>\d+)/rule/charset/create$', views.ViewRuleCharsetCreate.as_view(), name='ViewRuleCharsetCreate'),
    url(r'^policy/(?P<pid>\d+)/rule/charset/(?P<pk>\d+)/update$', views.ViewRuleCharsetUpdate.as_view(), name='ViewRuleCharsetUpdate'),
    url(r'^policy/(?P<pid>\d+)/rule/content/type$', views.ViewRuleContentTypeList.as_view(), name='ViewRuleContentTypeList'),
    url(r'^policy/(?P<pid>\d+)/rule/content/type/create$', views.ViewRuleContentTypeCreate.as_view(), name='ViewRuleContentTypeCreate'),
    url(r'^policy/(?P<pid>\d+)/rule/content/type/(?P<pk>\d+)/update$', views.ViewRuleContentTypeUpdate.as_view(), name='ViewRuleContentTypeUpdate'),
    url(r'^policy/(?P<pid>\d+)/rule/file/name$', views.ViewRuleFileNameList.as_view(), name='ViewRuleFileNameList'),
    url(r'^policy/(?P<pid>\d+)/rule/file/name/create$', views.ViewRuleFileNameCreate.as_view(), name='ViewRuleFileNameCreate'),
    url(r'^policy/(?P<pid>\d+)/rule/file/name/(?P<pk>\d+)/update$', views.ViewRuleFileNameUpdate.as_view(), name='ViewRuleFileNameUpdate'),
    url(r'^policy/(?P<pid>\d+)/rule/file/content$', views.ViewRuleFileContentList.as_view(), name='ViewRuleFileContentList'),
    url(r'^policy/(?P<pid>\d+)/rule/file/content/create$', views.ViewRuleFileContentCreate.as_view(), name='ViewRuleFileContentCreate'),
    url(r'^policy/(?P<pid>\d+)/rule/file/content/(?P<pk>\d+)/update$', views.ViewRuleFileContentUpdate.as_view(), name='ViewRuleFileContentUpdate'),
    url(r'^policy/(?P<pid>\d+)/rule/file/size/update$', views.ViewRuleFileSize.as_view(), name='ViewRuleFileSize'),
    
    # exclusions
    url(r'^policy/(?P<pid>\d+)/exclusions/domain$', views.ViewExclusionDomainList.as_view(), name='ViewExclusionDomainList'),
    url(r'^policy/(?P<pid>\d+)/exclusions/domain/create$', views.ViewExclusionDomainCreate.as_view(), name='ViewExclusionDomainCreate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/domain/(?P<pk>\d+)/update$', views.ViewExclusionDomainUpdate.as_view(), name='ViewExclusionDomainUpdate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/ip$', views.ViewExclusionIpList.as_view(), name='ViewExclusionIpList'),
    url(r'^policy/(?P<pid>\d+)/exclusions/ip/create$', views.ViewExclusionIpCreate.as_view(), name='ViewExclusionIpCreate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/ip/(?P<pk>\d+)/update$', views.ViewExclusionIpUpdate.as_view(), name='ViewExclusionIpUpdate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/range$', views.ViewExclusionRangeList.as_view(), name='ViewExclusionRangeList'),
    url(r'^policy/(?P<pid>\d+)/exclusions/range/create$', views.ViewExclusionRangeCreate.as_view(), name='ViewExclusionRangeCreate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/range/(?P<pk>\d+)/update$', views.ViewExclusionRangeUpdate.as_view(), name='ViewExclusionRangeUpdate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/subnet$', views.ViewExclusionSubnetList.as_view(), name='ViewExclusionSubnetList'),
    url(r'^policy/(?P<pid>\d+)/exclusions/subnet/create$', views.ViewExclusionSubnetCreate.as_view(), name='ViewExclusionSubnetCreate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/subnet/(?P<pk>\d+)/update$', views.ViewExclusionSubnetUpdate.as_view(), name='ViewExclusionSubnetUpdate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/url$', views.ViewExclusionUrlList.as_view(), name='ViewExclusionUrlList'),
    url(r'^policy/(?P<pid>\d+)/exclusions/url/create$', views.ViewExclusionUrlCreate.as_view(), name='ViewExclusionUrlCreate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/url/(?P<pk>\d+)/update$', views.ViewExclusionUrlUpdate.as_view(), name='ViewExclusionUrlUpdate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/content/type$', views.ViewExclusionContentTypeList.as_view(), name='ViewExclusionContentTypeList'),
    url(r'^policy/(?P<pid>\d+)/exclusions/content/type/create$', views.ViewExclusionContentTypeCreate.as_view(), name='ViewExclusionContentTypeCreate'),
    url(r'^policy/(?P<pid>\d+)/exclusions/content/type/(?P<pk>\d+)/update$', views.ViewExclusionContentTypeUpdate.as_view(), name='ViewExclusionContentTypeUpdate'),

    # members
    url(r'^policy/(?P<pid>\d+)/members/name$', views.ViewMemberNameList.as_view(), name='ViewMemberNameList'),
    url(r'^policy/(?P<pid>\d+)/members/name/create$', views.ViewMemberNameCreate.as_view(), name='ViewMemberNameCreate'),
    url(r'^policy/(?P<pid>\d+)/members/name/(?P<pk>\d+)/update$', views.ViewMemberNameUpdate.as_view(), name='ViewMemberNameUpdate'),
    url(r'^policy/(?P<pid>\d+)/members/ip$', views.ViewMemberIpList.as_view(), name='ViewMemberIpList'),
    url(r'^policy/(?P<pid>\d+)/members/ip/create$', views.ViewMemberIpCreate.as_view(), name='ViewMemberIpCreate'),
    url(r'^policy/(?P<pid>\d+)/members/ip/(?P<pk>\d+)/update$', views.ViewMemberIpUpdate.as_view(), name='ViewMemberIpUpdate'),
    url(r'^policy/(?P<pid>\d+)/members/range$', views.ViewMemberRangeList.as_view(), name='ViewMemberRangeList'),
    url(r'^policy/(?P<pid>\d+)/members/range/create$', views.ViewMemberRangeCreate.as_view(), name='ViewMemberRangeCreate'),
    url(r'^policy/(?P<pid>\d+)/members/range/(?P<pk>\d+)/update$', views.ViewMemberRangeUpdate.as_view(), name='ViewMemberRangeUpdate'),
    url(r'^policy/(?P<pid>\d+)/members/subnet$', views.ViewMemberSubnetList.as_view(), name='ViewMemberSubnetList'),
    url(r'^policy/(?P<pid>\d+)/members/subnet/create$', views.ViewMemberSubnetCreate.as_view(), name='ViewMemberSubnetCreate'),
    url(r'^policy/(?P<pid>\d+)/members/subnet/(?P<pk>\d+)/update$', views.ViewMemberSubnetUpdate.as_view(), name='ViewMemberSubnetUpdate'),

    url(r'^policy/(?P<pid>\d+)/members/ldap$', views.ViewMemberLdapList.as_view(), name='ViewMemberLdapList'),
    url(r'^policy/(?P<pid>\d+)/members/ldap/create$', views.ViewMemberLdapCreate.as_view(), name='ViewMemberLdapCreate'),
    url(r'^policy/(?P<pid>\d+)/members/ldap/(?P<pk>\d+)/update$', views.ViewMemberLdapUpdate.as_view(), name='ViewMemberLdapUpdate'),
    url(r'^policy/(?P<pid>\d+)/members/ldap/search$', views.ViewMemberLdapSearch.as_view(), name='ViewMemberLdapSearch'),
]