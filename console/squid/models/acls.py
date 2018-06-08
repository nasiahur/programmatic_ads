from django.db import models

#
# access controls
#
class AclDefault(models.Model):
    
    allowed_src          = models.TextField(blank=True)                    # list of src add to default localnet acl
    denied_src           = models.TextField(blank=True)                    # list of src that will not be able to use the proxy
    additional_sslports  = models.CharField(max_length=254,blank=True)     # additional ssl ports
    additional_safeports = models.CharField(max_length=254,blank=True)     # additional safe ports
    advanced_acl         = models.TextField(blank=True)                    # advanced acl written as-is
    advanced_access      = models.TextField(blank=True)                    # corresponding advanced http_access written as-is

    def as_array(self, contents):
        # converts a string from database as textfield into array of items
        array = []
        for line in contents.split('\n'):
            line = line.strip().strip('\r')
            if len(line) > 0:
                array.append(line)

        return array

    def get_allowed_src(self):
        return self.as_array(self.allowed_src)

    def get_denied_src(self):
        return self.as_array(self.denied_src)
