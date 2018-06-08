from django.db import models

#
#
#
from _domain.squid import SquidCacheDir

#
# abstract class for enum of log levels
#
class ReplacementPolicy(models.Model):

    class Meta:
        abstract = True

    LRU        = "lru"
    HEAP_GDSF  = "heap GDSF"
    HEAP_LFUDA = "heap LFUDA"
    HEAP_LRU   = "heap LRU"
    CHOICES = (
        (LRU, "lru"),
        (HEAP_GDSF, HEAP_GDSF),
        (HEAP_LFUDA, HEAP_LFUDA),
        (HEAP_LRU, HEAP_LRU)
    )


#
#
#
class MemoryCache(models.Model):

    cache_mem                     = models.IntegerField(default=256) # in MB
    maximum_object_size_in_memory = models.IntegerField(default=512) # in KB
    #NOT_MANAGED: memory_cache_shared
    #NOT_MANAGED: memory_cache_mode
    memory_replacement_policy     = models.CharField(max_length=32, choices=ReplacementPolicy.CHOICES,default=ReplacementPolicy.LRU)

#
#
#
class DiskCache(models.Model):

    enabled                  = models.BooleanField(default=False)
    cache_replacement_policy = models.CharField(max_length=32, choices=ReplacementPolicy.CHOICES,default=ReplacementPolicy.LRU)
    minimum_object_size      = models.IntegerField(default=0)    # in KB
    maximum_object_size      = models.IntegerField(default=4096) # in KB
    #NOT_MANAGED: store_dir_select_algorithm
    #NOT_MANAGED: max_open_disk_fds
    #NOT_MANAGED: cache_swap_low
    #NOT_MANAGED: cache_swap_high

    # cache_type
    CACHE_TYPE_UFS     = "ufs"
    CACHE_TYPE_CHOICES = (
        (CACHE_TYPE_UFS, CACHE_TYPE_UFS),
    )

    cache_type = models.CharField(max_length=32, choices=CACHE_TYPE_CHOICES,default=CACHE_TYPE_UFS)
    ufs_mb     = models.IntegerField(default=100) # in MB
    ufs_l1     = models.IntegerField(default=16)
    ufs_l2     = models.IntegerField(default=256)

    def cache_dir(self):
        return SquidCacheDir.get()

#
#
#
class RefreshPattern(models.Model):

    class Meta:
        ordering = ["regex"]

    insensitive = models.BooleanField(default=True)             # case insensitive matching
    regex       = models.TextField(blank=False)                 # regex to match
    min_time    = models.IntegerField(default=0)                # recommended 0 (minutes)
    percent     = models.IntegerField(default=20)               #
    max_time    = models.IntegerField(default=0)                # recommended 0 (minutes)

    # options
    override_expire        = models.BooleanField(default=False)
    override_lastmod       = models.BooleanField(default=False)
    reload_into_ims        = models.BooleanField(default=False)
    ignore_reload          = models.BooleanField(default=False)
    ignore_no_store        = models.BooleanField(default=False)
    ignore_must_revalidate = models.BooleanField(default=False)
    ignore_private         = models.BooleanField(default=False)
    ignore_auth            = models.BooleanField(default=False)
    max_stale              = models.BooleanField(default=False)
    max_stale_nn           = models.IntegerField(default=0)
    refresh_ims            = models.BooleanField(default=False)
    store_stale            = models.BooleanField(default=False)

    def get_options(self):

        options = []
        
        if self.override_expire:
            options.append("override_expire")

        if self.override_lastmod:
            options.append("override_lastmod")

        if self.reload_into_ims:
            options.append("reload_into_ims")

        if self.ignore_reload:
            options.append("ignore_reload")

        if self.ignore_no_store:
            options.append("ignore_no_store")

        if self.ignore_must_revalidate:
            options.append("ignore_must_revalidate")

        if self.ignore_private:
            options.append("ignore_private")

        if self.ignore_auth:
            options.append("ignore_auth")

        if self.max_stale:
            options.append("max_stale=%d" % self.max_stale_nn)

        if self.refresh_ims:
            options.append("refresh_ims")

        if self.store_stale:
            options.append("store_stale")

        if not len(options):
            return ""

        return " ".join(options)
