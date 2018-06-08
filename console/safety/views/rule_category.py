
#
#
#
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import Policy, CustomCategory, RuleCategory, RuleCategoryCustom, RuleDynamicCategory
from custom_categories import CustomCategorySyncer
from policy_items import PolicyMixin

#
#
#
class ViewRuleCategoryBuiltIn(SuccessMessageMixin, PolicyMixin, generic.edit.UpdateView):

    model  = RuleCategory
    fields = '__all__'
    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulecategorybuiltin_list.html"

    def get_object(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return policy.rulecategory

    def get_success_url(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return reverse_lazy("ViewRuleCategoryBuiltIn", kwargs={'pid':policy.pk})


#
#
#
class ViewRuleCategoryDynamic(SuccessMessageMixin, PolicyMixin, generic.edit.UpdateView):

    success_message = "need_squid_reload"
    template_name   = "safety/rules/rulecategorydynamic_list.html"
    fields          = [
        'enabled', 'analyze_request', 'analyze_response', 'classify_type',
        'classify_adult_themes_sexuality',
        'classify_drugs',
        'classify_gambling',
        'classify_nudity_pornography'
    ]

    def get_object(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return policy.ruledynamiccategory

    def get_success_url(self):
        policy = get_object_or_404(Policy, pk=self.kwargs['pid'])
        return reverse_lazy("ViewRuleCategoryDynamic", kwargs={'pid':policy.pk})

#
# special class that reads data from custom categories
#
class ViewRuleCategoryCustom(generic.View):

    def get(self, request, *args, **kwargs):

        # get policy
        policy = Policy.objects.get(pk=self.kwargs["pid"])

        # we must always sync file system -> custom categories table
        CustomCategorySyncer().sync_from_disk()

        # we MUST drop all category names which are not found in categories (happens when global custom category is removed)
        to_remove = []
        for activated in policy.rulecategorycustom_set.all():
            found = CustomCategory.objects.filter(name__startswith=activated.category)
            if len(found) == 0:
                to_remove.append(activated.category)

        # ok drop them all
        while len(to_remove) > 0:
            rule = policy.rulecategorycustom_set.all().filter(category=to_remove[0])
            rule.delete()
            to_remove = to_remove[1:]

        # create list of (name, title, enable) tuples out of category and rule block category
        categories = []
        for category in CustomCategory.objects.all():
            rule = policy.rulecategorycustom_set.filter(category__exact=category.pk)
            if len(rule) == 0:
                categories.append( (category.name, category.title, False) )
            elif len(rule) > 1:
                raise Exception("Unexpected error, more than 1 category of name %s was found in  RuleCustomCategory queryset" % category.name)
            else:
                categories.append( (category.name, category.title, [False, True][rule[0].enable]) )

        # raise the empty flag
        empty = len(categories) == 0

        # and render
        return render(request, "safety/rules/rulecategorycustom_list.html",  {'empty': empty, 'categories': categories, 'policy': policy})

    def category_is_on(self, category, postData):

        value = postData.get(category, "off")
        if value == "on":
            return True
        else:
            return False


    def post(self, request, *args, **kwargs):

        # mark as needing reload
        messages.info(self.request, "need_squid_reload")

        # get policy
        policy = Policy.objects.get(pk=self.kwargs["pid"])

        # get all categories
        for category in CustomCategory.objects.all():

            # see if this category is present in the rule
            rules = policy.rulecategorycustom_set.filter(category__exact=category.pk)

            if len(rules) == 0:

                # no, this rule is not present, see if user marked it as "on"
                if (self.category_is_on(category.name, request.POST)):
                    # yes, so add it
                    rule          = RuleCategoryCustom()
                    rule.policy   = policy
                    rule.category = category.name
                    rule.enable   = True
                    rule.save()
                else:
                    pass  # rule is not present and user did not switch it on, do nothing

            elif len(rules) == 1:

                # ok this rule is already present, switch it to "on" or "off" based on user selection
                rule        = rules[0]
                rule.enable = self.category_is_on(category.name, request.POST)
                rule.save()
            else:
                # strange situation more than 1 rules of the same category
                raise Exception("More than one rules of custom category %s found in policy %s" % (category, policy))

        return HttpResponseRedirect(reverse_lazy("ViewRuleCategoryCustom", kwargs={'pid':policy.pk}))

