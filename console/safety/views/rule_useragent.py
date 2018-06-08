import re

#
#
#
from django import forms
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import Policy, RuleUserAgent

#
#
#
from policy_items import PolicyMixin, ListViewEx

#
#
#
class ViewRuleUserAgentList(PolicyMixin, ListViewEx):

    model           = RuleUserAgent
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruleuseragent_list.html"

    def get_queryset(self):
        return RuleUserAgent.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("ViewRuleUserAgentList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class RuleUserAgentForm(forms.ModelForm):
    class Meta:
        model  = RuleUserAgent
        fields = '__all__'

    value = forms.CharField(max_length=512, widget=forms.TextInput(
        attrs={'size':'50','class':'input-block-level'})
    )
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )
    def clean_value(self):
        
        value = self.cleaned_data['value'].strip()
        try:
            p = re.compile(value)
        except Exception as e:
            raise forms.ValidationError("Specified Request User Agent regular expression cannot be compiled. Error: %s" % str(e))            
        return value


#
#
#
class ViewRuleUserAgentCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    model           = RuleUserAgent
    form_class      = RuleUserAgentForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruleuseragent_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleUserAgentList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ViewRuleUserAgentUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    model           = RuleUserAgent
    form_class      = RuleUserAgentForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruleuseragent_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleUserAgentList", kwargs={'pid':self.kwargs['pid']})
