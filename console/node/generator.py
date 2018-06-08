#
#
#
import os
import shutil

#
# domain
#
from _domain.utils import FileWriter, JsonDumper

#
#
#
from node.models import Sharing

#
#
#
class Generator(object):

    #
    #
    #
    def __init__(self, root_dir):

        self.root_dir = root_dir

    def generate(self):

        self.generate_config(self.root_dir)



    #
    #
    #
    def generate_config(self, target_dir):

        # create writer and dumper
        w = FileWriter(target_dir)        
        d = JsonDumper()

        # generate all global files
        self.generate_sharing(w, d)
        
    #
    #
    #
    def generate_sharing(self, writer, dumper):

        sharing = Sharing.objects.first()
        d = { 
            'upload_recategorization'   : sharing.upload_recategorization,
            'upload_telemetry_basic'    : sharing.upload_telemetry_basic,
            'upload_telemetry_extended' : sharing.upload_telemetry_extended
        }
        writer.write('sharing.json', dumper.dumps(d))
