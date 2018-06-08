#
#
#
from _domain.squid import LdapGroupSearcher, LdapUserSearcher

#
#
#
from django.views import generic

#
#
#
from safety.models import Policy, MemberLdap
from squid.models import AuthAd

#
#
#
from member_base import *
from policy_items import PolicyMixin

#
#
#
class ViewMemberLdapList(ViewMemberList):

    model         = MemberLdap
    template_name = "safety/members/ldap_list.html"

#
#
#
class MemberLdapForm(forms.ModelForm):

    name    = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'size':'50','class':'input-block-level'}))
    dn      = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'size':'50','class':'input-block-level'}))
    comment = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'size':'90', 'rows':'3', 'class':'input-block-level'}),required=False)

    class Meta:
        model = MemberLdap    
        fields = '__all__'

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
#
#
def get_groups(request):

    pattern = request.GET.get('search', '')
    domain  = AuthAd.objects.first()

    # construct some params
    use_ldaps = False
    if domain.lookup_mode in (AuthAd.LOOKUP_MODE_LDAP, AuthAd.LOOKUP_MODE_GC):
        use_ldaps = False
    if domain.lookup_mode in (AuthAd.LOOKUP_MODE_LDAPS, AuthAd.LOOKUP_MODE_GCS):
        use_ldaps = True

    # create the searcher
    searcher = LdapGroupSearcher(
        domain.dc1addr,         # dc host name or ip address
        domain.lookup_mode,     # port to bind to
        use_ldaps,              # if use ldaps:// schema or not
        domain.base_dn,         # the dn to start looking from
        domain.bind_user,       # name of the user to bind as
        domain.bind_pass        # his password
    )

    # and do the find
    return searcher.find_groups(pattern)



#
#
#
class ViewMemberLdapCreate(ViewMemberCreate):

    model           = MemberLdap
    form_class      = MemberLdapForm
    template_name   = "safety/members/ldap_form.html"

    def get_context_data(self, **kwargs):
        
        context = super(ViewMemberLdapCreate, self).get_context_data(**kwargs)
        context['groups'] = get_groups(self.request)
        return context

#
#
#
class ViewMemberLdapUpdate(ViewMemberUpdate):

    model           = MemberLdap
    form_class      = MemberLdapForm
    template_name   = "safety/members/ldap_form.html"

    def get_context_data(self, **kwargs):
        
        context = super(ViewMemberLdapUpdate, self).get_context_data(**kwargs)
        context['groups'] = get_groups(self.request)
        return context

#
#
#
class ViewMemberLdapSearch(PolicyMixin, generic.TemplateView):

    template_name = "safety/members/ldap_search.html"

    def get_context_data(self, **kwargs):
        context = super(ViewMemberLdapSearch, self).get_context_data(**kwargs)
        policy  = Policy.objects.get(pk=self.kwargs['pid'])

        context['groups'] = policy.memberldap_set.all()

        # get the parameters
        action = self.request.GET.get('action', '').strip()
        group  = self.request.GET.get('group', '').strip()
        user   = self.request.GET.get('user', '').strip()
        in_all = self.request.GET.get('all', '').strip()

        # highlight the selected group
        if len(group) > 0:
            try:
                context['selected_group_pk'] = int(group)
            except:
                pass

        # highlight the user
        if len(user) > 0:
            context['selected_user'] = user

        # now to the search
        if len(group) > 0 and len(user) > 0:

            s = LdapUserSearcher(AuthAd.objects.first())
            g = []

            # if we need to search for all groups, add all
            if len(in_all) > 0:
                for item in policy.memberldap_set.all():
                    g.append(item)
            else:
                g.append(policy.memberldap_set.get(pk=group))

            context['search_result'] = s.find_user(g, user)

        return context
