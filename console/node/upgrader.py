import os

#
#
#
from _domain.utils import read_json_array, read_json_object

#
#
#
from node.models import Sharing


#
#
#
class SharingImporter:

    def upgrade(self, etc_dir):

        path = os.path.join(etc_dir, "safety", "sharing.json")
        
        if not os.path.exists(path):            
            path = os.path.join(etc_dir, "node", "sharing.json")
            
            if not os.path.exists(path):
                return

        self.upgrade_impl(read_json_object(path))

    def upgrade_impl(self, data):

        obj = Sharing.objects.first()

        obj.upload_recategorization   = data.get("upload_recategorization", False)
        obj.upload_telemetry_basic    = data.get("upload_telemetry_basic", False)
        obj.upload_telemetry_extended = data.get("upload_telemetry_extended", False)

        obj.save()

#
#
#
class Upgrader(object):

    def __init__(self, major, minor):

        self.major   = major
        self.minor   = minor

    def upgrade(self, etc_dir):

        SharingImporter().upgrade(etc_dir)        
