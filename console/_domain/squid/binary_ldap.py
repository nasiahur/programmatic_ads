import os

#
#
#
from _domain.core import Paths, System

#
#
#
class BinaryLdap:

    @staticmethod
    def full_path():

    	name = "ldap"
    	if System.name() == System.WS_WINDOWS:
    		name += ".exe"

    	return os.path.join(Paths.bin_dir(), name)

