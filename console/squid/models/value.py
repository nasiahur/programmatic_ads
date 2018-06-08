from django.db import models

#
# value model
#
class ValueModel(models.Model):

    class Meta:
        
        abstract = True 
        ordering = ["value"]

    value   = models.CharField(max_length=254, unique=True)
    comment = models.TextField(blank=True)

