#
#
#
import os

#
#
#
from _domain.utils import Command

#
#
#
from binary_ldap import BinaryLdap

#
#
#
class LdapTester:
    
    def run(self):

        try:        
            (exit_code, stdout, stderr) = Command().run( 
                [ BinaryLdap.full_path(), "--test"]
            )
            return { 'exit_code' : exit_code, 'stdout' : stdout, 'stderr' : stderr }
        except Exception as e:
            return { 'exit_code' : 1, 'stdout' : '', 'stderr' : str(e) }

