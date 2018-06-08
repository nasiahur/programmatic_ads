import os
import traceback
#
#
#
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy

#
#
#
from _domain.core import Paths
from _domain.squid import SquidCacheInitializer

#
#
#
from squid.models import MemoryCache, DiskCache
from squid.generator import Generator

#
#
#
class ViewCacheMemory(SuccessMessageMixin, generic.edit.UpdateView):

    model           = MemoryCache
    fields          = ['cache_mem', 'maximum_object_size_in_memory', 'memory_replacement_policy']
    template_name   = 'squid/cache/memory.html'
    success_message = 'need_squid_restart'

    def get_object(self):
        return MemoryCache.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewCacheMemory')


#
#
#
class ViewCacheDisk(SuccessMessageMixin, generic.edit.UpdateView):

    model           = DiskCache
    fields          = ['cache_replacement_policy', 'minimum_object_size', 'maximum_object_size', 'cache_type', 'ufs_mb']
    template_name   = 'squid/cache/disk.html'
    success_message = 'need_squid_restart'

    def get_object(self):
        return DiskCache.objects.first()
    
    def get_success_url(self): 
        return reverse_lazy('ViewCacheDisk')

#
#
#
class ViewCacheDiskEnable(generic.View):

    success_message = "need_squid_restart"
    
    def post(self, request, *args, **kwargs):

        diskcache = DiskCache.objects.first()
        value     = request.POST.get('enabled', '0')
        if value == '1':
            diskcache.enabled = True
        else:
            diskcache.enabled = False
        
        diskcache.save()
        
        messages.info(self.request, self.success_message)   

        return HttpResponseRedirect(reverse_lazy("ViewCacheDisk"))


#
#
#
class DiskResetForm(forms.Form):
    confirm = forms.CharField()
    
    def clean_confirm(self):

        value = self.cleaned_data['confirm']
        value = value.strip()
        value = value.upper()

        if value != "I CONFIRM":
            raise forms.ValidationError("Please type 'I confirm' in this field if you agree to erase and re-initialize the cache dir.")

        return value

#
#
#
class ViewCacheDiskReset(SuccessMessageMixin, generic.edit.FormView):
    
    template_name   = 'squid/cache/disk_reset.html'
    form_class      = DiskResetForm
    success_message = 'need_squid_restart'

    
    def get_success_url(self): 
        return reverse_lazy('ViewCacheDisk')

    def get_context_data(self, **kwargs):
        
        context = super(ViewCacheDiskReset, self).get_context_data(**kwargs)    
        context['disk_cache'] = DiskCache.objects.first()
        return context

    def form_valid(self, form):

        try:

            # ok the user wants us to reset the cache
            disk_cache = DiskCache.objects.first()

            # first we must enable the cache in the database
            disk_cache.enabled = True
            disk_cache.save()

            # now we generate the squid configuration on disk
            g = Generator(
                os.path.join(Paths.etc_dir(), "squid")
            )
            g.generate()

            # and we call special sudoing binary that will stop squid, reset the cache and start squid again
            SquidCacheInitializer().initialize()

            # perfect now we have the cache enabled and reinitialized, return nicely
            return super(ViewCacheDiskReset, self).form_valid(form)
            
        except Exception as e:        
            form.errors['__all__'] = form.error_class([
                "%s\n%s" % (str(e), traceback.format_exc()) 
            ])

            # failure
            return super(ViewCacheDiskReset, self).form_invalid(form)

