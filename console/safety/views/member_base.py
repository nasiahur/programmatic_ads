#
# domain
#
from _domain.utils import LicenseManager

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
# generic list of members
#
class ViewMemberList(PolicyMixin, ListViewEx):

    success_message = "need_squid_reload"
    
    def get_queryset(self):
        return self.model.objects.filter(policy_id=self.kwargs["pid"])

    def get_success_url(self):
        return reverse_lazy("View" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})

    def get_context_data(self, **kwargs):

        context = super(ViewMemberList, self).get_context_data(**kwargs)
        policy  = Policy.objects.get(pk=self.kwargs['pid'])

        context['count_of_names']    = policy.membername_set.all().count()
        context['count_of_ips']      = policy.memberip_set.all().count()
        context['count_of_ranges']   = policy.memberrange_set.all().count()
        context['count_of_subnets']  = policy.membersubnet_set.all().count()
        context['count_of_groups']   = policy.memberldap_set.all().count()

        # assume we have non home license
        is_home = False

        # get the license type
        (result, param2) = LicenseManager().get()
        if result is True:
            license = param2
            if license['type'] == "home":
                is_home = True

        # and set the context
        context['is_home'] = is_home

        return context

#
# generic member form
#
class MemberForm(forms.ModelForm):
    
    value   = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'size':'50','class':'input-block-level'}))
    comment = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),required=False)

    def clean_value(self):
        value = self.cleaned_data['value']
        value = value.strip()
        return value

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
# generic member create view
#
class ViewMemberCreate(PolicyMixin, SuccessMessageMixin, generic.edit.CreateView):

    success_message = "need_squid_reload"

    def get_success_url(self):
        return reverse_lazy("View" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})

#
# generic member update view
#
class ViewMemberUpdate(PolicyMixin, SuccessMessageMixin, generic.edit.UpdateView):

    success_message = "need_squid_reload"
    
    def get_success_url(self):
        return reverse_lazy("View" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})
