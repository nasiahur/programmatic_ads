import os
import json
import time
import traceback

#
# business logic
#
from _domain.core import Paths
from _domain.utils import CommandElevated

#
# django
#
from django.views import generic
from django.shortcuts import render
from django.conf import settings

#
# our
#
from frame.models import Profile

#
#
#
class ApplyView(generic.TemplateView):

    template_name = "frame/apply.html"

    def get_context_data(self, **kwargs):
        context = super(ApplyView, self).get_context_data(**kwargs)
        context['hide_apply'] = True

        return context

#
#
#
class CommandRestart:

    def run(self, only_reload):

        name = "restart.sh"
        if only_reload:
            name = "reload.sh"

        args = [os.path.join(Paths.bin_dir(), name)]
        
        return CommandElevated().run(args)

#
#
#
class RestartReloadViewBase(generic.View):

    def post(self, request, *args, **kwargs):

        is_reload  = self.only_reload
        hide_apply = True

        try:
            # generate configuration on disk
            profile           = Profile.objects.first()
            profile.version   = profile.version + 1
            profile.timestamp = int(round(time.time() * 1000))
            profile.save()
            profile.generate()

            # and run the restart/reload command
            (exit_code, stdout, stderr) = CommandRestart().run(self.only_reload)
            if exit_code == 0:
                return render(request, 'frame/apply_success.html', locals())
            else:
                return render(request, 'frame/apply_failure.html', locals())

        except Exception as exception:
            all_locals = locals()
            all_locals['traceback'] = traceback.format_exc()
            return render(request, 'frame/apply_failure.html', all_locals)

#
#
#
class ReloadView(RestartReloadViewBase):
    only_reload = True

#
#
#
class RestartView(RestartReloadViewBase):
    only_reload = False
