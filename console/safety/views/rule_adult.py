from django import forms
from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


#
#
#
from safety.models import Policy, RuleAdult

#
#
#
from policy_items import PolicyMixin


class RuleAdultForm(forms.ModelForm):
    
    class Meta:
        model  = RuleAdult
        fields = [
            'trust_allowed_categories',
            'enable_heuristics', 
            'heuristics_maximum_weight',
            'enable_phrases', 
            'phrases_maximum_weight', 
            'phrases_maximum_size',
            'phrases_scan_links',
            'phrases_scan_javascript',
            'phrases_scan_css',
            'phrases_parse_links',
            'enable_image_filtering'
        ]
        
    phrases_maximum_weight = forms.CharField(max_length=512, widget=forms.TextInput(
        attrs={'size':'50','class':'input-block-level'})
    )
    
    def clean_heuristics_maximum_weight(self):        
        v = self.cleaned_data['heuristics_maximum_weight']
        n = None
        
        try:
            n = int(v)
        except Exception as e:
            raise forms.ValidationError("The value cannot be converted to integer. Error: %s" % (str(e)))            
        
        if n <= 0 or n > 9999:
            raise forms.ValidationError("The maximum weight if inspected text must be within [1:9999] interval. The value %d is invalid." % (n) )            
        return n
    
    def clean_phrases_maximum_weight(self):        
        phrases_maximum_weight = self.cleaned_data['phrases_maximum_weight']
        try:
            phrases_maximum_weight = int(phrases_maximum_weight)
        except Exception as e:
            raise forms.ValidationError("The value cannot be converted to integer. Error: %s" % (str(e)))            
        
        if phrases_maximum_weight <= 0 or phrases_maximum_weight > 9999:
            raise forms.ValidationError("The maximum weight if inspected text must be within [1:9999] interval. The value %s is invalid." % (phrases_maximum_weight) )            
        return phrases_maximum_weight

#
#
#
class ViewRuleAdult(SuccessMessageMixin, PolicyMixin, generic.edit.UpdateView): 

    success_message = "need_squid_reload"
    model           = RuleAdult
    form_class      = RuleAdultForm
    template_name   = "safety/rules/ruleadult_form.html"


    def get_success_url(self):
        return reverse_lazy("ViewRuleAdult", kwargs={'pid':self.kwargs['pid']})

    def get_object(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return policy.ruleadult
