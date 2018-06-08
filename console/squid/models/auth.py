import os

#
#
#
from _domain.core import Paths

#
#
#
from django.db import models

#
# manual IP <-> user name mappings
#
class AuthLabel(models.Model):

    enable = models.BooleanField(default=False)

    resolve_ip_as_user_name = models.BooleanField(default=False)
                    # if set to true we try to reverse resolve the ip address to user_name
                    # this is good in the fixed IP scenario when no authentication on proxy
                    # is implemented but each device has its own fixed (reserved) IP


class AuthLabelUsers(models.Model):

    user_name = models.CharField(max_length=254, unique=True)
    user_ip   = models.CharField(max_length=254, blank=True)
    user_mac  = models.CharField(max_length=254, blank=True)
    comment   = models.TextField(blank=True)

#
# local database authentication settings 
#
class AuthLocalDb(models.Model):

    enable          = models.BooleanField(default=False)
    title           = models.CharField(max_length=254, default='Squid Proxy')
    helper_verbose  = models.BooleanField(default=False)
    helper_total    = models.IntegerField(default=20)
    helper_idle     = models.IntegerField(default=10)
    helper_startup  = models.IntegerField(default=5)

#
# radius authentication settings
#
class AuthRadius(models.Model):

    enable          = models.BooleanField(default=False)    
    server          = models.CharField(max_length=254)
    secret          = models.CharField(max_length=254)
    title           = models.CharField(max_length=254, default='Squid Proxy')
    helper_verbose  = models.BooleanField(default=False)
    helper_total    = models.IntegerField(default=20)
    helper_idle     = models.IntegerField(default=10)
    helper_startup  = models.IntegerField(default=5)

#
# Pseudo Active Directory authentication (IP -> user name mapping using https://github.com/diladele/active-directory-inspector project)
#
class AuthPseudoAd(models.Model):

    enable          = models.BooleanField(default=False)
    server1         = models.CharField(max_length=254)
    port1           = models.IntegerField(default=8443)
    server2         = models.CharField(max_length=254, blank=True)
    port2           = models.IntegerField(default=8443)
    token           = models.CharField(max_length=254, blank=True)
    positive_ttl    = models.IntegerField(default=600)
    negative_ttl    = models.IntegerField(default=300)
    helper_verbose  = models.BooleanField(default=False)
    helper_total    = models.IntegerField(default=20)
    helper_idle     = models.IntegerField(default=10)
    helper_startup  = models.IntegerField(default=5)


#
# Active Directory authentication settings 
#
class AuthAd(models.Model):

    # active directory integration settings    
    LOOKUP_MODE_LDAP    = 389
    LOOKUP_MODE_LDAPS   = 636
    LOOKUP_MODE_GC      = 3268
    LOOKUP_MODE_GCS     = 3269
    LOOKUP_MODE_CHOICES = (
        (LOOKUP_MODE_LDAP,  "LDAP over port 389 (default)"), 
        (LOOKUP_MODE_LDAPS, "LDAPS over port 636 (encrypted)"), 
        (LOOKUP_MODE_GC,    "Global Catalog LDAP over port 3268 (multi-domain)"), 
        (LOOKUP_MODE_GCS,   "Global Catalog LDAPS over port 3269 (multi-domain, encrypted)"),
    )

    realm       = models.CharField(max_length=254)
    dc1addr     = models.CharField(max_length=254)
    dc2addr     = models.CharField(max_length=254, blank=True)
    base_dn     = models.CharField(max_length=254)
    bind_user   = models.CharField(max_length=254)
    bind_pass   = models.CharField(max_length=254)
    lookup_mode = models.IntegerField(choices=LOOKUP_MODE_CHOICES,default=LOOKUP_MODE_LDAP)
    
    # ldap group membership lookup settings 
    cachetime = models.IntegerField(default=300)  # number of seconds to cache LDAP search results before contacting the LDAP server again
    timeout   = models.IntegerField(default=10)   # connect and search timeout in seconds

    # basic ldap authentication scheme
    ldap_enable          = models.BooleanField(default=False)
    ldap_title           = models.CharField(max_length=254, default='Squid Proxy')
    ldap_credsttl        = models.IntegerField(default=5) # minutes
    ldap_helper_verbose  = models.BooleanField(default=False)
    ldap_helper_total    = models.IntegerField(default=20)
    ldap_helper_idle     = models.IntegerField(default=10)
    ldap_helper_startup  = models.IntegerField(default=5)

    # ntlm authentication scheme
    ntlm_enable          = models.BooleanField(default=False)
    ntlm_helper_verbose  = models.BooleanField(default=False)
    ntlm_helper_total    = models.IntegerField(default=20)
    ntlm_helper_idle     = models.IntegerField(default=10)
    ntlm_helper_startup  = models.IntegerField(default=5)

    # kerberos authentication scheme
    krb5_enable          = models.BooleanField(default=False)
    krb5_spn             = models.CharField(max_length=254)   # e.g. HTTP/proxy.example.lan@EXAMPLE.LAN
    krb5_use_gssnoname   = models.BooleanField(default=False) # if yes no spn is needed
    krb5_no_replay_cache = models.BooleanField(default=False) # sets KRB5RCACHETYPE=none - it speeds up the Kerberos authentication
    krb5_helper_verbose  = models.BooleanField(default=False)
    krb5_helper_total    = models.IntegerField(default=70)
    krb5_helper_idle     = models.IntegerField(default=25)
    krb5_helper_startup  = models.IntegerField(default=10)
    
    def keytab_exists(self):        
        keytab = os.path.join(Paths.etc_dir(), "krb5.keytab")
        if os.path.isfile(keytab):
            return True
        return False

    def keytab_path(self):
        if not self.keytab_exists():
            return "<NOT AVAILABLE>"
        return os.path.join(Paths.etc_dir(), "krb5.keytab")

