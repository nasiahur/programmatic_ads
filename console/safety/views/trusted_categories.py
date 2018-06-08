#
#
#
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from safety.models import Categories

#
#
#
class ViewSettingsTrustedCategories(SuccessMessageMixin, generic.edit.UpdateView):

    model  = Categories
    fields = '__all__'
    success_message = "need_squid_restart"
    template_name   = "safety/settings/categories_form.html"

    def get_object(self):
        return Categories.objects.first()

    def get_success_url(self):
        return reverse_lazy("ViewSettingsTrustedCategories")


    