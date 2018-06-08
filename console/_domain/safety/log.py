import os

#
#
#
from _domain.core import Paths
from _domain.utils import FileReader

#
#
#
class ErrorLog:

    def get(self):

    	path = os.path.join(Paths.var_dir(), "log", "error.log")
    	try:
        	return FileReader(path).read()
        except Exception as e:
        	return "%s does not exist or is not accessible, error - %s" % (path, str(e))

#
#
#
class UpdateLog:

    def get(self):
    	
    	path = os.path.join(Paths.var_dir(), "log", "cron_update.log")
    	try:
        	return FileReader(path).read()
        except Exception as e:
        	return "%s does not exist or is not accessible, error - %s" % (path, str(e))