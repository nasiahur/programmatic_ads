#
#
#
from _domain.core import Paths, Build, Distrib, System
from _domain.safety import ErrorLog
from _domain.utils import Version, FolderInfo

#
#
#
from django.views import generic

#
#
#
class ViewSafetySystemInfo(generic.TemplateView):

    template_name = "safety/support/system.html"

    def get_context_data(self, **kwargs):
        
        context = super(ViewSafetySystemInfo, self).get_context_data(**kwargs)

        v = Version()

        info = {
            'product_name'      : 'Web Safety for Squid Proxy',
            'installed_version' : v.installed,
            'latest_version'    : v.latest,
            'need_to_upgrade'   : v.need_to_upgrade(),        # 0 - no_need_to_upgrade, 1 - may_upgrade, 2 - should_upgrade, 3 - must_upgrade
            'whats_new'         : v.whats_new
        };
        context['info'] = info

        # add hardcoded settings
        context['WEBSAFETY_ETC_DIR']      = Paths.etc_dir()
        context['WEBSAFETY_ETC_DIR_SIZE'] = long(FolderInfo(Paths.etc_dir()).get_size()) 
        context['WEBSAFETY_VAR_DIR']      = Paths.var_dir()
        context['WEBSAFETY_VAR_DIR_SIZE'] = long(FolderInfo(Paths.var_dir()).get_size())
        context['WEBSAFETY_BIN_DIR']      = Paths.bin_dir()
        context['WEBSAFETY_BIN_DIR_SIZE'] = long(FolderInfo(Paths.bin_dir()).get_size())
        context['WEBSAFETY_VERSION']      = Build.version()
        context['WEBSAFETY_ARCH']         = Distrib.arch()
        context['WEBSAFETY_DISTRIB']      = Distrib.name()
        context['WEBSAFETY_SYSTEM']       = System.name()
        
        return context

#
#
#
class ViewSafetyErrorLog(generic.TemplateView):

    template_name = "safety/support/error_log.html"

    def get_context_data(self, **kwargs):
        context = super(ViewSafetyErrorLog, self).get_context_data(**kwargs)
        context['error_log'] = ErrorLog().get()
        return context