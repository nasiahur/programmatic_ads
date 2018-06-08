from django import forms
from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


#
#
#
from safety.models import Policy, RuleApps

#
#
#
from policy_items import PolicyMixin


#
#
#
class RuleAppsForm(forms.ModelForm):
    
    class Meta:
        model  = RuleApps
        fields = '__all__'

#
#
#
class ViewRuleApps(SuccessMessageMixin, PolicyMixin, generic.edit.UpdateView): 

    success_message = "need_squid_reload"
    model           = RuleApps
    form_class      = RuleAppsForm
    template_name   = "safety/rules/ruleapps_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleApps", kwargs={'pid':self.kwargs['pid']})

    def get_object(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return policy.ruleapps