import re
#
#
#
from django import forms
from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import Policy, FileType, RuleFileContent

#
#
#
from policy_items import PolicyMixin, ListViewEx

#
#
#
class ViewRuleFileContentList(PolicyMixin, ListViewEx):

    model           = RuleFileContent
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulefilecontent_list.html"

    def get_queryset(self):
        return RuleFileContent.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("ViewRuleFileContentList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class RuleFileContentForm(forms.ModelForm):

    value = forms.CharField(max_length=512, widget=forms.TextInput(
        attrs={'size':'50','class':'input-block-level'})
    )
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )

    class Meta:
        model  = RuleFileContent
        fields = '__all__'

    def clean_value(self):
        value = self.cleaned_data['value'].strip()
        
        try:
            o = get_object_or_404(FileType, name=value)
        except Exception as e:
            raise forms.ValidationError("The specified value was not found in list of available Real File Content names.")            
        return value
        

#
#
#
class ViewRuleFileContentCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    model           = RuleFileContent
    form_class      = RuleFileContentForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulefilecontent_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleFileContentList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ViewRuleFileContentUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    model           = RuleFileContent
    form_class      = RuleFileContentForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulefilecontent_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleFileContentList", kwargs={'pid':self.kwargs['pid']})
