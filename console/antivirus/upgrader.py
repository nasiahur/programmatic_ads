import os

#
#
#
from _domain.utils import read_json_array, read_json_object

#
#
#
from antivirus.models import SafeBrowsing


#
#
#
class SafeBrowsingImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "antivirus", "safe_browsing.json")
        
        if not os.path.exists(path):            
            return

        self.upgrade_impl(read_json_object(path))

    def upgrade_impl(self, data):

        obj = SafeBrowsing.objects.first()

        obj.enable              = data.get("enable", False)
        obj.bypass_to_localnet  = data.get("bypass_to_localnet", False)
        obj.api_key             = data.get("api_key", "")
        obj.deny_url            = data.get("deny_url", "")
        obj.check_malware       = data.get("check_malware", True)
        obj.check_social        = data.get("check_social", True)
        obj.check_unwanted_soft = data.get("check_unwanted_soft", False)
        obj.cache_clean         = data.get("cache_clean", 0)
        obj.daemon_port         = data.get("daemon_port", 18890)
        obj.helper_verbose      = data.get("helper_verbose", False)
        obj.helper_total        = data.get("helper_total", 20)
        obj.helper_idle         = data.get("helper_idle", 10)
        obj.helper_startup      = data.get("helper_startup", 5)
        
        obj.save()

#
#
#
class Upgrader(object):

    def __init__(self, major, minor):

        self.major   = major
        self.minor   = minor

    def upgrade(self, etc_dir):

        SafeBrowsingImporter().upgrade(etc_dir)        
