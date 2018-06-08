#
#
#
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

#
#
#
from _domain.utils import LicenseManager

#
#
#
from node.models import Sharing

#
#
#
class ViewDataChoices(SuccessMessageMixin, generic.edit.UpdateView):

    template_name   = "node/tools/sharing.html"
    success_message = "need_squid_restart"
    model           = Sharing
    fields          = '__all__'

    def get_success_url(self):
        return reverse_lazy("node:ViewDataChoices")

    def get_object(self):
        return Sharing.objects.first()

    def form_valid(self, form):

        # check to see if we have community license key
        try:

            # check license
            (result, param2) = LicenseManager().get()

            # ok license check succeeded
            if result is True:

                # for convinience
                license = param2

                # see if it is valid
                if license["valid"] == "1":

                    # in community license we always enable sharing
                    if license['type'] == "community":
                        
                        form.instance.upload_recategorization = True
                        form.instance.upload_telemetry_basic  = True

        except Exception as e:
            pass

        return super(ViewDataChoices, self).form_valid(form)
