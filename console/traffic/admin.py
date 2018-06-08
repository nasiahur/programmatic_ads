from django.contrib import admin

from traffic.models import *

# Register your models here.
admin.site.register(Monitoring)
admin.site.register(WsMgrd)
admin.site.register(Reporter)
admin.site.register(Job)
admin.site.register(Event)