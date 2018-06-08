from django.db import models


#
# abstract class for enum of log levels
#
class LogLevel(models.Model):

    class Meta:
        abstract = True

    LOG_LEVEL_FATAL   = 0
    LOG_LEVEL_ERROR   = 1
    LOG_LEVEL_WARNING = 2
    LOG_LEVEL_INFO    = 3
    LOG_LEVEL_DEBUG   = 6
    LOG_LEVEL_VDEBUG  = 9
    LOG_LEVEL_CHOICES = (
        (LOG_LEVEL_FATAL, "Fatal"),
        (LOG_LEVEL_ERROR, "Errors"),
        (LOG_LEVEL_WARNING, "Warnings"),
        (LOG_LEVEL_INFO, "Informational"),
        (LOG_LEVEL_DEBUG, "Debug"),
        (LOG_LEVEL_VDEBUG, "Debug (Verbose)"),
    )


#
#
#
class TroubleShooting(models.Model):

    loglevel_section_all = models.IntegerField(choices=LogLevel.LOG_LEVEL_CHOICES,default=LogLevel.LOG_LEVEL_ERROR)

#
#
#
class LogSection(models.Model):

    section_id      = models.IntegerField(unique=True, primary_key=True)
    title           = models.CharField(max_length=200)
    comment         = models.CharField(max_length=200, default="", blank=True)
    level           = models.IntegerField(choices=LogLevel.LOG_LEVEL_CHOICES,default=LogLevel.LOG_LEVEL_ERROR)

    def __str__(self):
        return self.title
