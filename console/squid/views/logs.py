#
#
#
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy


#
# domain logic (non django)
#
from _domain.squid import SquidAccessLog, SquidCacheLog
from squid.models import TroubleShooting, LogSection, LogLevel

#
# 
#
class ViewLog(generic.base.TemplateView):

    def get_context_data(self, **kwargs):

        context = super(ViewLog, self).get_context_data(**kwargs)        

        # get size, include and exclude strings from request
        include = self.request.GET.get('include', '')
        exclude = self.request.GET.get('exclude', '')
        size    = 256
        try:
            size = int(self.request.GET.get('size', '256'))
            if size > 1024:
                size = 1024
        except Exception, e:
            pass

        # save into context
        context['size']         = size
        context['include']      = include
        context['exclude']      = exclude
        context['log_contents'] = self.get_contents(size, include, exclude)
        context['log_size']     = self.get_size()

        return context

    def get_size(self):

        log  = self.log_class()
        size = log.get_size()
       
        return size

    def get_contents(self, line_count, include, exclude):

        log      = self.log_class()
        contents = log.get_contents(line_count, include, exclude)
        if not contents:
            contents = "Requested log file is empty."
        
        return contents

#
#
#
class ViewAccessLog(ViewLog):

    template_name = "squid/logs/access_log.html"
    log_class     = SquidAccessLog

#
#
#
class ViewCacheLog(ViewLog):

    template_name = "squid/logs/cache_log.html"
    log_class     = SquidCacheLog

#
#
#
class ViewLogLevels(SuccessMessageMixin, generic.edit.UpdateView):

    model           = TroubleShooting
    fields          = ['loglevel_section_all']
    template_name   = 'squid/logs/levels.html'
    success_message = 'need_squid_restart'

    def get_object(self):
        return TroubleShooting.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewLogLevels')

    def get_context_data(self, **kwargs):

        context = super(ViewLogLevels, self).get_context_data(**kwargs)  
        context['sections'] = LogSection.objects.all().order_by("section_id")
        return context

    def propagate_all_sections(self, level):

        for section in LogSection.objects.all():

            section.level = level
            section.save()


    def form_valid(self, form):

        # save the form into the database
        result = super(ViewLogLevels, self).form_valid(form)

        # get the updated troubleshooting object from the database
        troubleshooting = TroubleShooting.objects.first()

        # changing all level *always* resets the individual levels
        self.propagate_all_sections(troubleshooting.loglevel_section_all)

        # see if the reset_defaults is present
        if 'reset_defaults' in self.request.POST:

            # oh yes, reset the all section
            troubleshooting.loglevel_section_all = LogLevel.LOG_LEVEL_ERROR
            troubleshooting.save()

            # and propagate
            self.propagate_all_sections(troubleshooting.loglevel_section_all)
            
        # and return successfully
        return result


#
#
#
class ViewLogSectionUpdate(SuccessMessageMixin, generic.edit.UpdateView):

    model           = LogSection
    fields          = ['level']
    template_name   = 'squid/logs/section.html'
    success_message = 'need_squid_restart'

    def get_success_url(self): 
        return reverse_lazy('ViewLogLevels')
