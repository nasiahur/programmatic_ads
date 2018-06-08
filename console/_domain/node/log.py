#
#
#
import os

#
#
#
from _domain.core import Paths
from _domain.utils import FileReader

#
#
#
class SyncLog:

    def get(self):
    	
        path = os.path.join(Paths.var_dir(), "log", "wssyncd.log")
        try:
            return FileReader(path).read()
        except Exception as e:
            return "%s does not exist yet or is not accessible, error - %s" % (path, str(e))
