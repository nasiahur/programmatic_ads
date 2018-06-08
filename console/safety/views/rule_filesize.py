from django import forms
from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


#
#
#
from safety.models import Policy, RuleFileSize

#
#
#
from policy_items import PolicyMixin


#
#
#
class RuleFileSizeForm(forms.ModelForm):

    class Meta:
        model  = RuleFileSize
        fields = [
            'enable', 'max_size'
        ]

    def clean_max_size(self):
        value = self.cleaned_data['max_size']
        
        try:
            if value <= 4096:
                raise Exception()
        except:
            raise forms.ValidationError("Maximum file size must be > 4096.")            
        return value
       

#
#
#
class ViewRuleFileSize(SuccessMessageMixin, PolicyMixin, generic.edit.UpdateView): 

    success_message = "need_squid_reload"
    model           = RuleFileSize
    form_class      = RuleFileSizeForm
    template_name   = "safety/rules/rulefilesize_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleFileSize", kwargs={'pid':self.kwargs['pid']})

    def get_object(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return policy.rulefilesize