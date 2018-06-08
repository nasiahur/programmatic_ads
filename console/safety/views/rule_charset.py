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
from safety.models import Policy, RuleCharset

#
#
#
from policy_items import PolicyMixin, ListViewEx

#
#
#
class ViewRuleCharsetList(PolicyMixin, ListViewEx):

    model           = RuleCharset
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulecharset_list.html"

    def get_queryset(self):
        return RuleCharset.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("ViewRuleCharsetList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class RuleCharsetForm(forms.ModelForm):

    value = forms.CharField(max_length=512, widget=forms.TextInput(
        attrs={'size':'50','class':'input-block-level'})
    )
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )

    class Meta:
        model  = RuleCharset
        fields = '__all__'
        
    def clean_value(self):
        return self.cleaned_data['value'].strip()
        

#
#
#
class ViewRuleCharsetCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    model           = RuleCharset
    form_class      = RuleCharsetForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulecharset_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleCharsetList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ViewRuleCharsetUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    model           = RuleCharset
    form_class      = RuleCharsetForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulecharset_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleCharsetList", kwargs={'pid':self.kwargs['pid']})
