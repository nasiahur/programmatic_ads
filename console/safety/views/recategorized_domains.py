import json
#
#
#
from _domain.safety import DomainCategorizer, BuildInCategories

#
#
#
from django import forms
from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import RecategorizedDomain
from utility.views import ListViewTransposer

#
#
#
from items import ViewItemList

#
#
#
class ViewRecategorizedDomains(SuccessMessageMixin, ViewItemList):

    model           = RecategorizedDomain
    success_message = "need_squid_reload"
    template_name   = 'safety/settings/recategorizeddomain_list.html'

    def get_success_url(self):
        return reverse("ViewRecategorizedDomains")

#
#
#
class RecategorizedDomainForm(forms.ModelForm):

    class Meta:
        model = RecategorizedDomain
        fields = '__all__'
        #widgets = {
        #    'categories': forms.CheckboxSelectMultiple(attrs={'class': 'recategorized_categories'}),
        #}

    def clean_name(self):

        value = self.cleaned_data['name']
        value = value.strip()
        if value.startswith("."):
            raise forms.ValidationError("Error: domain name cannot start with dot. Recategorization is only possible for fully specified domain names. Any possible subdomain of a recategorized domain automatically inherits its categories from parent.")

        return value

    def clean(self):

        at_least_one_set = False

        # check the user set at least one category
        for name in BuildInCategories.CATEGORY_NAMES:

            attrname = "assign_%s" % name
            value    = self.cleaned_data.get(attrname, False)
            if value:
                at_least_one_set = True
        
        if not at_least_one_set:
            raise forms.ValidationError("Error: please select at least one category for recategorized domain.")

        return self.cleaned_data
    

#
#
#
class ViewRecategorizedDomainCreate(SuccessMessageMixin, generic.View):

    success_message = "need_squid_reload"

    def get(self, request, *args, **kwargs):

        known  = []
        domain = self.request.GET.get('name', '')
        if len(domain) > 0:

            known = DomainCategorizer().categorize(domain)            
            if len(known) > 0:
                # lookup object id and redirect to update page
                try:
                    objects = RecategorizedDomain.objects.filter(name=domain)
                    if len(objects) > 0:
                        return HttpResponseRedirect(reverse('ViewRecategorizedDomainUpdate', kwargs={'pk':objects[0].pk}))
                except RecategorizedDomain.DoesNotExist:
                    pass

        # build up the initial dict
        initial = {}
        for category in known:
            initial["assign_%s" % category] = True

        # construct the form
        form = RecategorizedDomainForm(initial=initial)

        # and render it
        return render(self.request, 'safety/settings/recategorizeddomain_form.html', { 'form': form, 'name' : domain, 'known' : known})

    def post(self, request, *args, **kwargs):

        form = RecategorizedDomainForm(self.request.POST)
        if form.is_valid():

            # lookup possibly existing object
            d = None

            objects = RecategorizedDomain.objects.filter(name=form.cleaned_data['name'])
            if len(objects) > 0:
                d = objects[0]
            else:
                d = RecategorizedDomain(name=form.cleaned_data['name'])
                d.save()

            # see if any category is set by the user
            for name in BuildInCategories.CATEGORY_NAMES:

                attrname = "assign_%s" % name
                assiged  = form.cleaned_data.get(attrname, False)
                if assiged:
                    # yes user wants to assign this category
                    setattr(d, attrname, True)
                else:
                    # no user does not want to assign this category
                    setattr(d, attrname, False)

            # and save the object
            d.save()

            # good, add success message
            messages.info(self.request, self.success_message)

            # and redirect
            return HttpResponseRedirect(reverse('ViewRecategorizedDomains'))
        else:
            print form.errors

        return render(self.request, 'safety/settings/recategorizeddomain_form.html', { 'form': form })

#
#
#
class ViewRecategorizedDomainUpdate(SuccessMessageMixin, generic.edit.UpdateView):

    success_message = "need_squid_reload"
    model           = RecategorizedDomain
    form_class      = RecategorizedDomainForm
    template_name   = 'safety/settings/recategorizeddomain_form.html'

    def get_context_data(self, **kwargs):
        context = super(ViewRecategorizedDomainUpdate, self).get_context_data(**kwargs)
        context['create'] = False
        return context

    def get_success_url(self):
        return reverse("ViewRecategorizedDomains")

