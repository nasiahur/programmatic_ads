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
from safety.models import Policy, RuleContentType

#
#
#
from policy_items import PolicyMixin, ListViewEx

#
#
#
class ViewRuleContentTypeList(PolicyMixin, ListViewEx):

    model           = RuleContentType
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulecontenttype_list.html"

    def get_queryset(self):
        return RuleContentType.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("ViewRuleContentTypeList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class RuleContentTypeForm(forms.ModelForm):

    value = forms.CharField(max_length=512, widget=forms.TextInput(
        attrs={'size':'50','class':'input-block-level'})
    )
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )

    class Meta:
        model  = RuleContentType
        fields = '__all__'
        
    def clean_value(self):
        value = self.cleaned_data['value'].strip()
        
        try:
            (part1, part2) = value.split("/")                
        except:
            raise forms.ValidationError("Specified Content Type value should be written as string/string, for example image/gif.")            
        return value.lower()
        

#
#
#
class ViewRuleContentTypeCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    model           = RuleContentType
    form_class      = RuleContentTypeForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulecontenttype_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleContentTypeList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ViewRuleContentTypeUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    model           = RuleContentType
    form_class      = RuleContentTypeForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulecontenttype_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleContentTypeList", kwargs={'pid':self.kwargs['pid']})
