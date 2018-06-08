from django import forms
from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


#
#
#
from safety.models import Policy, RuleAnnoyances

#
#
#
from policy_items import PolicyMixin

#
#
#
class RuleAnnoyancesForm(forms.ModelForm):
    class Meta:
        model  = RuleAnnoyances
        fields = [
            'block_ads', 'protect_privacy'
        ]


#
#
#
class ViewRuleAnnoyances(SuccessMessageMixin, PolicyMixin, generic.edit.UpdateView): 

    success_message = "need_squid_reload"
    model           = RuleAnnoyances
    form_class      = RuleAnnoyancesForm
    template_name   = "safety/rules/ruleannoyances_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleAnnoyances", kwargs={'pid':self.kwargs['pid']})

    def get_object(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return policy.ruleannoyances

