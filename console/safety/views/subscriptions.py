#
#
#
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from _domain.safety import UpdateLog, DefinitionsFactory
from safety.models  import Annoyances


#
#
#
class ViewSubscriptionsAdBlock(SuccessMessageMixin, generic.edit.UpdateView):

    model  = Annoyances
    fields = [
        'enable_bulgarian',
        'enable_chinese',
        'enable_czech',
        'enable_danish',
        'enable_dutch',
        'enable_english',
        'enable_estonian',
        'enable_french',
        'enable_german',
        'enable_greek',
        'enable_hungarian',
        'enable_indian',
        'enable_israeli',
        'enable_italian',
        'enable_japanese',
        'enable_korean',
        'enable_latvian',
        'enable_lithuanian',
        'enable_polish',
        'enable_portuguese',
        'enable_romanian',
        'enable_russian',
        'enable_slovak',
        'enable_spanish',
        'enable_swedish',
        'enable_turkish',
        'enable_vietnamese',
        'enable_custom1'
    ]
    success_message = "need_squid_restart"
    template_name   = "safety/subscriptions/adblock_form.html"

    def get_object(self):
        return Annoyances.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewSubscriptionsAdBlock")

#
#
#
class ViewSubscriptionsPrivacy(SuccessMessageMixin, generic.edit.UpdateView):

    model  = Annoyances
    fields = [
        'enable_adware',
        'enable_annoyance',
        'enable_antiadb',
        'enable_cookies',
        'enable_privacy',
        'enable_social',
        'enable_tracking',
        'enable_custom2'
    ]
    success_message = "need_squid_restart"
    template_name   = "safety/subscriptions/privacy_form.html"

    def get_object(self):
        return Annoyances.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewSubscriptionsPrivacy")

#
#
#
class ViewSubscriptionsAdvanced(SuccessMessageMixin, generic.edit.UpdateView):

    model  = Annoyances
    fields = [
        'apply_replace_heuristics',
        'replace_with_image',
        'hide_tags',
        'mangle_id',
        'mangle_class',
        'scan_external_links'
    ]
    success_message = "need_squid_restart"
    template_name   = "safety/subscriptions/advanced_form.html"

    def get_object(self):
        return Annoyances.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewSubscriptionsAdvanced")


        
#
#
#
class ViewSafetyUpdateLog(generic.TemplateView):

    template_name = "safety/subscriptions/update_log.html"

    def get_context_data(self, **kwargs):
        context = super(ViewSafetyUpdateLog, self).get_context_data(**kwargs)
        context['update_log'] = UpdateLog().get()
        context['info']       = DefinitionsFactory().get()
        return context