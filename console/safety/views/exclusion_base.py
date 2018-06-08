#
# django
#
from django import forms
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
# ours
#
from safety.models import Policy

#
# implementation
#
from policy_items import PolicyMixin, ListViewEx


#
# generic list of exclusions
#
class ViewExclusionList(PolicyMixin, ListViewEx):

    success_message = "need_squid_reload"
    
    def get_queryset(self):
        return self.model.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("View" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})

    def get_context_data(self, **kwargs):

        context = super(ViewExclusionList, self).get_context_data(**kwargs)
        policy  = Policy.objects.get(pk=self.kwargs['pid'])

        context['count_of_domains']  = policy.exclusiondomain_set.all().count()
        context['count_of_ips']      = policy.exclusionip_set.all().count()
        context['count_of_ranges']   = policy.exclusionrange_set.all().count()
        context['count_of_subnets']  = policy.exclusionsubnet_set.all().count()
        context['count_of_urls']     = policy.exclusionurl_set.all().count()
        context['count_of_ctypes']   = policy.exclusioncontenttype_set.all().count()

        return context

#
# generic exclusion form
#
class ExclusionForm(forms.ModelForm):
    
    value           = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'size':'50','class':'input-block-level'}))
    scan_adult      = forms.BooleanField(required=False)
    scan_categories = forms.BooleanField(required=False)
    scan_custom     = forms.BooleanField(required=False)
    scan_file       = forms.BooleanField(required=False)
    scan_adblock    = forms.BooleanField(required=False)
    scan_privacy    = forms.BooleanField(required=False)
    scan_http       = forms.BooleanField(required=False)
    comment         = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),
        required=False
    )

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 0:
            # check to see the comment does not have unicode symbols
            try:
                comment_str = str(comment)
            except Exception as e:
                raise forms.ValidationError("Comment can only contain ASCII symbols. Error '%s'." % (str(e),) )
        return comment

#
# generic exclusion create view
#
class ViewExclusionCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    success_message = "need_squid_reload"

    def get_success_url(self):
        return reverse_lazy("View" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})

#
# generic exclusion update view
#
class ViewExclusionUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    success_message = "need_squid_reload"
    
    def get_success_url(self):
        return reverse_lazy("View" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})
