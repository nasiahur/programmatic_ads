#
#
#
from django import forms
from django.views import generic
from django.db.models import Max
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import Policy, Advanced, RuleAnnoyances, RuleAdult, RuleApps, RuleFileSize, RuleCategory, RuleDynamicCategory
from squid.models import BumpMode

#
#
#
class PolicyList(generic.ListView):

    def get_queryset(self):
        return Policy.objects.all().order_by('-priority')

    def get_context_data(self, **kwargs):

        context  = super(PolicyList, self).get_context_data(**kwargs)
        context['bumpmode'] = BumpMode.objects.first()
        return context

#
#
#
class PolicyForm(forms.ModelForm):

    class Meta:

        model  = Policy
        fields = ['name']
        
    name = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'size':'50','class':'input-block-level'}))

    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)
    
    def clean_name(self):

        name = self.cleaned_data['name'].strip().lower()
        if not self.is_ascii(name):
            raise forms.ValidationError("Policy '%s' cannot be added, becase it contains non ASCII alphanumeric characters." % name)

        objects = Policy.objects.filter(name__exact=name)
        if objects != None and len(objects) > 0:
            raise forms.ValidationError("Policy '%s' already exists." % name)
            
        banned = ["&", "/", "\\"]
        for c in banned:
            if name.find(c) != -1:
                raise forms.ValidationError("Policy name cannot contain characters %s" % (",".join(banned)))
            
        return name

#
#
#
class View_PolicyCreate(SuccessMessageMixin, generic.edit.CreateView):

    model           = Policy
    form_class      = PolicyForm
    success_url     = reverse_lazy('ViewPolicyList')
    success_message = "need_squid_reload"

    def form_valid(self, form):

        # get the policy
        policy = form.instance

        # get current maximum priority
        max_priority = Policy.objects.all().aggregate(Max('priority'))['priority__max']

        # assign the app for the new policy instance
        policy.priority = max_priority + 1
        
        # save the form, it also saves the policy
        form.save()

        # create corresponding one-to-one rules
        policy.advanced = Advanced(policy=policy, enable=False, comment="New filtering policy. Specify meaningful comment here. Please adjust this policy settings and enable it afterwards.")
        policy.advanced.save()

        policy.ruleannoyances = RuleAnnoyances(policy=policy)
        policy.ruleannoyances.save()

        policy.ruleadult = RuleAdult(policy=policy)
        policy.ruleadult.save()

        policy.ruleapps = RuleApps(policy=policy)
        policy.ruleapps.save()

        policy.rulefilesize = RuleFileSize(policy=policy)
        policy.rulefilesize.save()

        policy.rulecategory = RuleCategory(policy=policy)
        policy.rulecategory.save()

        policy.ruledynamiccategory = RuleDynamicCategory(policy=policy)
        policy.ruledynamiccategory.save()

        # and call the base class
        return super(View_PolicyCreate, self).form_valid(form)

#
#
#
class View_PolicyMoveUp(generic.View):

    def post(self, request, *args, **kwargs):

        # get current policy
        policies = Policy.objects.filter(pk=self.kwargs['pid'])
        if len(policies) != 1:
            raise Exception("Cannot get policy by id")

        policy = policies[0]
        if policy.priority == 0:
            raise Exception("Cannot increase priority from zero")

        # get first policy with priority higher than ours
        objects = Policy.objects.order_by('priority').filter(priority__gt=policy.priority)
        if len(objects) >= 1:

            if objects[0].priority == 0:
                raise Exception("Unexpected priority of 0 found")

            old_priority        = objects[0].priority
            objects[0].priority = policy.priority
            policy.priority     = old_priority
            policy.save()
            objects[0].save()

        messages.info(self.request, "need_squid_reload")

        return HttpResponseRedirect(reverse("ViewPolicyList"))

#
#
#
class View_PolicyCopy(SuccessMessageMixin, generic.edit.CreateView):

    model           = Policy
    form_class      = PolicyForm
    template_name   = 'safety/policy_copy.html'
    success_message = 'need_squid_reload'

    def get_context_data(self, **kwargs):

        context  = super(View_PolicyCopy, self).get_context_data(**kwargs)
        context['policy'] = Policy.objects.get(pk=self.kwargs['pid'])
        return context

    def form_valid(self, form):

        # get the farm and old policy
        old    = Policy.objects.get(pk=self.kwargs['pid'])
        policy = form.instance

        # get current maximum priority
        max_priority = Policy.objects.all().aggregate(Max('priority'))['priority__max']

        # assign the references and priority
        policy.priority = max_priority + 1
        
        # save the form, it also saves the policy
        form.save()

        # get attributes from old policy
        old_rule_adult        = old.ruleadult
        old_rule_annoyances   = old.ruleannoyances
        old_rule_apps         = old.ruleapps
        old_rule_filesize     = old.rulefilesize
        old_rule_category     = old.rulecategory
        old_rule_dyn_category = old.ruledynamiccategory
        old_rule_ccategory    = old.rulecategorycustom_set
        old_rule_domain       = old.ruledomain_set
        old_rule_url          = old.ruleurl_set
        old_advanced          = old.advanced

        # copy all exclusions
        exclusions = [
            old.exclusiondomain_set,
            old.exclusionip_set,
            old.exclusionrange_set,
            old.exclusionsubnet_set,
            old.exclusionurl_set,
            old.exclusioncontenttype_set,
        ]

        # and members
        members = [
            old.membername_set,
            old.memberip_set,
            old.memberrange_set,
            old.membersubnet_set,
            old.memberldap_set
        ]

        # and files
        files = [
            old.rulecontenttype_set,
            old.rulecharset_set,
            old.rulefilename_set,
            old.rulefilecontent_set
        ]

        # and schedules
        schedules = [
            old.schedule_set
        ]

        # create rules
        rule_adult          = old_rule_adult
        rule_adult.pk       = None
        rule_adult.policy   = policy
        rule_adult.save()

        rule_annoyances        = old_rule_annoyances
        rule_annoyances.pk     = None
        rule_annoyances.policy = policy
        rule_annoyances.save()

        rule_apps           = old_rule_apps
        rule_apps.pk        = None
        rule_apps.policy    = policy
        rule_apps.save()

        rule_filesize        = old_rule_filesize
        rule_filesize.pk     = None
        rule_filesize.policy = policy
        rule_filesize.save()

        rule_category        = old_rule_category
        rule_category.pk     = None
        rule_category.policy = policy
        rule_category.save()

        rule_dynamic_category        = old_rule_dyn_category
        rule_dynamic_category.pk     = None
        rule_dynamic_category.policy = policy
        rule_dynamic_category.save()

        advanced            = old_advanced
        advanced.pk         = None
        advanced.policy     = policy
        advanced.save()

        for c in old_rule_ccategory.all():
            rule_block_ccategory        = c
            rule_block_ccategory.pk     = None
            rule_block_ccategory.policy = policy
            rule_block_ccategory.save()

        for c in old_rule_domain.all():
            r        = c
            r.pk     = None
            r.policy = policy
            r.save()

        for c in old_rule_url.all():
            r        = c
            r.pk     = None
            r.policy = policy
            r.save()

        # copy all exclusions
        for exclusion_set in exclusions:
            for exclusion in exclusion_set.all():
                e = exclusion
                e.pk = None
                e.policy = policy
                e.save()

        # copy all members
        for member_set in members:
            for member in member_set.all():
                m = member
                m.pk = None
                m.policy = policy
                m.save()

        # copy all files
        for file_set in files:
            for file in file_set.all():
                f = file
                f.pk = None
                f.policy = policy
                f.save()

        # copy all schedules
        for schedule_set in schedules:
            for schedule in schedule_set.all():
                s = schedule
                s.pk = None
                s.policy = policy
                s.save()

        # and call the base class
        return super(View_PolicyCopy, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ViewPolicyList")



#
#
#
class ViewPolicyDelete(generic.edit.DeleteView):

    model           = Policy
    success_url     = reverse_lazy("ViewPolicyList")
    success_message = "need_squid_reload"

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(ViewPolicyDelete, self).delete(request, *args, **kwargs)