#
#
#
from django import forms
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse

#
#
#
from safety.models import Policy, Advanced

#
#
#
from policy_items import PolicyMixin

#
#
#
class AdvancedForm(forms.ModelForm):

    class Meta:
        model  = Advanced
        fields = ['enable', 'sslbump', 'tunnel_block', 'comment', 'exclude_by_referer', 'ignore_case', 'hide_history', 'hide_result_info']
        
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )


#
#
#
class ViewAdvanced(SuccessMessageMixin, PolicyMixin, generic.edit.UpdateView):

    model           = Advanced
    form_class      = AdvancedForm
    success_message = "need_squid_reload"

    def get_object(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return policy.advanced

    def get_success_url(self):
        return reverse_lazy("ViewAdvanced", kwargs={'pid': self.kwargs['pid']})

    def form_valid(self, form):

        if form.instance.policy.name == 'default':
            form.instance.enable = True

        return super(ViewAdvanced, self).form_valid(form)