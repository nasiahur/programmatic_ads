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
from utility.generator import BaseGenerator
from antivirus.models  import SafeBrowsing

#
#
#
class Generator(BaseGenerator):

    #
    #
    #
    def __init__(self, root_dir):

        # call the base class
        super(Generator, self).__init__(root_dir)

    #
    #
    #
    def generate_config(self, target_dir):

        # create writer and dumper
        w = FileWriter(target_dir)        
        d = JsonDumper()

        self.generate_safebrowsing(w, d)

    #
    #
    #
    def generate_safebrowsing(self, writer, dumper):

        o = SafeBrowsing.objects.first()
        d = {
            "enable"              : o.enable, 
            "bypass_to_localnet"  : o.bypass_to_localnet, 
            "api_key"             : o.api_key,
            "deny_url"            : o.deny_url,
            "check_malware"       : o.check_malware,
            "check_social"        : o.check_social,
            "check_unwanted_soft" : o.check_unwanted_soft,
            "cache_clean"         : o.cache_clean,
            "daemon_port"         : o.daemon_port,
            "helper_verbose"      : o.helper_verbose,
            "helper_total"        : o.helper_total,
            "helper_idle"         : o.helper_idle,
            "helper_startup"      : o.helper_startup
        }
        writer.write('safe_browsing.json', dumper.dumps(d))

