#
#
#
from django.db import models

#
#
#
from .value import ValueModel


#
#
#
class BumpMode(models.Model):
    
    BUMPMODE_SELECTED = 0
    BUMPMODE_BUMPALL  = 1
    BUMPMODE_CHOICES  = (
        (BUMPMODE_SELECTED, "Only selected HTTPS domains"),
        (BUMPMODE_BUMPALL, "All HTTPS domains, except specified")
    )

    value = models.IntegerField(default=BUMPMODE_SELECTED,choices=BUMPMODE_CHOICES)

#
#
#
class SslTargetDomain(ValueModel):
    pass 
    
class SslTargetIp(ValueModel):
    pass

class SslTargetSubnet(ValueModel):
    pass

class SslErrorDomain(ValueModel):
    pass

class SslErrorIp(ValueModel):
    pass

class SslErrorSubnet(ValueModel):
    pass

#
#
#
class SslIntermediateCert(models.Model):

    class Meta:
        ordering = ["subject"]
    
    serial_num    = models.CharField(max_length=254)
    subject_keyid = models.CharField(max_length=254, unique=True)
    subject       = models.CharField(max_length=254)
    common_name   = models.CharField(max_length=254)
    alt_names     = models.CharField(max_length=254)
    valid_from    = models.CharField(max_length=254)
    valid_until   = models.CharField(max_length=254)
    issuer        = models.CharField(max_length=254)
    pem           = models.TextField(blank=False)