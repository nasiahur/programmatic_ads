#
#
#
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import Policy


#
#
#
class PolicyMixin(object):

    def get_context_data(self, **kwargs):

        context = super(PolicyMixin, self).get_context_data(**kwargs)
        policy  = get_object_or_404(Policy, pk = self.kwargs['pid'])
        context['policy'] = policy
        return context

#
#
#
class DeleteViewEx(generic.edit.DeleteView):
	
    success_message = ""
    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(DeleteViewEx, self).delete(request, *args, **kwargs)

#
#
#
class ListViewEx(generic.ListView):

    def post(self, request, *args, **kwargs):

        for selected_id in request.POST.getlist('selected_id'):
            item = get_object_or_404(self.model, pk = selected_id)
            item.delete()

        messages.info(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())


#
#
#
class UpdateViewEx(SuccessMessageMixin, PolicyMixin, generic.edit.UpdateView):
    pass

#
#
#
class View_PolicyItemUpdate(UpdateViewEx):

    success_message = "need_squid_reload"
    
    def get_success_url(self):
        return reverse("View_" + self.model.__name__, kwargs={'pid':self.kwargs['pid'], 'pk':self.kwargs['pk']})

#
#
#
class View_PolicyItemUpdateRedirectToList(UpdateViewEx):

    success_message = "need_squid_reload"

    def get_success_url(self):
        return reverse("View_" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})

#
#
#
class CreateViewEx(SuccessMessageMixin, generic.edit.CreateView):
    pass


#
#
#
class ItemCreateViewEx(PolicyMixin, CreateViewEx):

    success_message="need_squid_reload"
    def get_success_url(self):
        return reverse_lazy("View_" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})


#
#
#
#class View_PolicyItemCreateRedirectToList(ItemCreateViewEx):
#    success_message = "need_squid_reload"
#
#    def get_success_url(self):
#        return reverse_lazy("View_" + self.model.__name__ + "List", kwargs={'pid':self.kwargs['pid']})