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
from safety.models import Policy, RuleDomain

#
#
#
from policy_items import PolicyMixin, ListViewEx

#
#
#
class ViewRuleDomainList(PolicyMixin, ListViewEx):

    model           = RuleDomain
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruledomain_list.html"

    def get_queryset(self):
        return RuleDomain.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("ViewRuleDomainList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class RuleDomainForm(forms.ModelForm):

    class Meta:
        model  = RuleDomain
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
                
        if "?" in value or "*" in value:
            raise forms.ValidationError("Domain '%s' cannot be added, becase it contains wildcards which are not supported." % (value) )

        value = self.clean_non_ascii(value)
            
        return value.lower()

    def clean_non_ascii(self, original_value):
        if len(original_value) > 0:
            # check to see the comment does not have unicode symbols
            try:
                value_str = str(original_value)
            except Exception as e:
                raise forms.ValidationError("Value can only contain ASCII symbols. Error '%s'." % (str(e),) )
        return original_value

#
#
#
class ViewRuleDomainCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    model           = RuleDomain
    form_class      = RuleDomainForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruledomain_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleDomainList", kwargs={'pid':self.kwargs['pid']})

#
#
#
class ViewRuleDomainUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    model           = RuleDomain
    form_class      = RuleDomainForm
    success_message = "need_squid_reload"
    template_name   = "safety/rules/ruledomain_form.html"

    def get_success_url(self):
        return reverse_lazy("ViewRuleDomainList", kwargs={'pid':self.kwargs['pid']})
