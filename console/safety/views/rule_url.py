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
from safety.models import Policy, RuleUrl

#
#
#
from policy_items import PolicyMixin, ListViewEx

#
#
#
class ViewRuleUrlList(PolicyMixin, ListViewEx):

    model           = RuleUrl
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruleurl_list.html"

    def get_queryset(self):
        return RuleUrl.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("ViewRuleUrlList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class RuleUrlForm(forms.ModelForm):
    class Meta:
        model  = RuleUrl
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
            raise forms.ValidationError("Specified Request URL regular expression cannot be compiled. Error: %s" % str(e))            
        return value

#
#
#
class ViewRuleUrlCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    model           = RuleUrl
    form_class      = RuleUrlForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruleurl_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleUrlList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ViewRuleUrlUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    model           = RuleUrl
    form_class      = RuleUrlForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruleurl_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleUrlList", kwargs={'pid':self.kwargs['pid']})
