from django.contrib import admin

# register your models here.
from squid.models import *

admin.site.register(BumpMode)
admin.site.register(SslTargetDomain)
admin.site.register(SslTargetIp)
admin.site.register(SslTargetSubnet)
admin.site.register(SslErrorDomain)
admin.site.register(SslErrorIp)
admin.site.register(SslErrorSubnet)
admin.site.register(SslIntermediateCert)

# various global settings
admin.site.register(Administrative)
admin.site.register(Dns)
admin.site.register(Network)
admin.site.register(TroubleShooting)
admin.site.register(LogSection)

# cache settings
admin.site.register(MemoryCache)
admin.site.register(DiskCache)

# exclusions
admin.site.register(ExcludeDomainName)
admin.site.register(ExcludeDomainIp)
admin.site.register(ExcludeDomainSubnet)
admin.site.register(ExcludeDomainRange)
admin.site.register(ExcludeUserIp)
admin.site.register(ExcludeUserSubnet)
admin.site.register(ExcludeUserRange)
admin.site.register(ExcludeUserAgent)
admin.site.register(ExcludeContentType)
admin.site.register(ExcludeSchedule)
admin.site.register(ExcludeAdvanced)

# auth
admin.site.register(AuthLabel)
admin.site.register(AuthLabelUsers)
admin.site.register(AuthLocalDb)
admin.site.register(AuthRadius)
admin.site.register(AuthAd)
admin.site.register(AuthPseudoAd)

# access controls
admin.site.register(AclDefault)