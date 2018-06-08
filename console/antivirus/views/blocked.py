import os

#
#
#
from django.views import generic
from django.http  import HttpResponse
from django.template import Context, Template

#
#
#
from _domain.core import Paths, Build

#
#
#
class ViewSafeBrowsingBlocked(generic.View):

    def get(self, request, *args, **kwargs):            

        # construct the path
        path = os.path.join(Paths.etc_dir(), "blocked_safe_browsing.html")

        # run it all in the exception block
        try:

            # get the file
            with open(path, "r") as fin:
                contents = fin.read()

            # render everything
            templ   = Template(contents)
            context = {
                "VERSION"     : Build.version(),
                "URI"         : request.GET.get('url', ''),
                "RESULT_INFO" : request.GET.get('reason', '')
            }

            # and return response
            response = HttpResponse(templ.render(Context(context)), content_type="text/html")
            
            return response

        except Exception as e:

            return HttpResponse(str(e), content_type="text/html")