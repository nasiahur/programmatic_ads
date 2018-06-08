#
#
#
from django import forms
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy

#
#
#
from .forms import DomainNameForm

#
#
#
class ViewItemList(generic.ListView):

    success_message = "need_squid_reload"
    
    def post(self, request, *args, **kwargs):

        # drop all items by pk
        for selected_id in request.POST.getlist('selected_id'):
            item = get_object_or_404(self.model, pk=selected_id)
            item.delete()

        # tell the user squid needs to be reloaded or restarted            
        messages.info(self.request, self.success_message)

        # and redirect to success url
        return HttpResponseRedirect(self.get_success_url())


#
#
#
class ViewItemCreate(SuccessMessageMixin, generic.edit.CreateView):

    success_message = "need_squid_reload"

#
#
#
class ViewDomainNameCreate(ViewItemCreate):

    def form_valid(self, form):

        try:
            # squid treats .google.com and google.com as the same, so we need to change the uniqueness
            value  = form.cleaned_data['value']
            value1 = value
            if value1.startswith("."):
                value1 = value1[1:]
            else:
                value1 = "." + value

            # see if value1 already exists
            d = self.model.objects.filter(value=value1)
            if d is None or len(d) == 0:

                # ok this values does not exist, tell form is valid
                return super(ViewDomainNameCreate, self).form_valid(form)

            # if we got here such value already exists, so fail the form validation
            raise Exception(
                "Domain '%s' cannot be added, becase similar domain '%s' already exists. Squid considers these domains as same." % (value, value1) 
            )

        except Exception as e:        
            form.errors['__all__'] = form.error_class(["%s" % str(e)])

            # failure
            return super(ViewDomainNameCreate, self).form_invalid(form)


#
#
#
class ViewItemUpdate(SuccessMessageMixin, generic.edit.UpdateView):

    success_message = "need_squid_reload"

