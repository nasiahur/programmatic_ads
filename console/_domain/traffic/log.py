import os

#
#
#
from _domain.core import Paths
from _domain.utils import FileReader

#
#
#
class ReportLog:

    def get(self):

    	path = os.path.join(Paths.var_dir(), "log", "report.log")
    	try:
        	return FileReader(path).read()
        except Exception as e:
        	return "%s does not exist or is not accessible, error - %s" % (path, str(e))

#
#
#
class MonitorLog:

    def get(self):

        path = os.path.join(Paths.var_dir(), "log", "wsmgrd.log")
        try:
            return FileReader(path).read()
        except Exception as e:
            return "%s does not exist or is not accessible, error - %s" % (path, str(e))

class DatabaseLog:

    def get(self):

        path = os.path.join(Paths.var_dir(), "log", "database.log")
        try:
            return FileReader(path).read()
        except Exception as e:
            return "%s does not exist or is not accessible, error - %s" % (path, str(e))

