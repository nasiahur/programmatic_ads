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
from safety.models import Policy, RuleFileName

#
#
#
from policy_items import PolicyMixin, ListViewEx

#
#
#
class ViewRuleFileNameList(PolicyMixin, ListViewEx):

    model           = RuleFileName
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulefilename_list.html"

    def get_queryset(self):
        return RuleFileName.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("ViewRuleFileNameList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class RuleFileNameForm(forms.ModelForm):

    value = forms.CharField(max_length=512, widget=forms.TextInput(
        attrs={'size':'50','class':'input-block-level'})
    )
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )

    class Meta:
        model  = RuleFileName
        fields = '__all__'

    def clean_value(self):
        value = self.cleaned_data['value'].strip()
        
        try:
            p = re.compile(value)
        except Exception as e:
            raise forms.ValidationError("Specified File Name regular expression cannot be compiled. Error: %s" % str(e))            
        return value.lower()
        

#
#
#
class ViewRuleFileNameCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    model           = RuleFileName
    form_class      = RuleFileNameForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulefilename_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleFileNameList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ViewRuleFileNameUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    model           = RuleFileName
    form_class      = RuleFileNameForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulefilename_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleFileNameList", kwargs={'pid':self.kwargs['pid']})
