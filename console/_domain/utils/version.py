import json

#
#
#
from _domain.core import Build, Distrib

#
#
#
from downloader import FileDownloader


#
#
#
class Version:
    
    def __init__(self):

        downloader      = FileDownloader(Build.version(), Distrib.arch())
        self.installed  = Build.version()
        
        try:
            content = downloader.download_file("https://defs.diladele.com/websafety/version/%s/" % Distrib.name())
            data    = json.loads(content)

            self.latest         = data['current']
            self.whats_new      = data['whats_new_txt']
            self.whats_new_html = data['whats_new_html']
            self.whats_new_md   = data['whats_new_md']

        except Exception as e:

            self.latest         = "!ERROR OCCURRED! %s" % str(e)
            self.whats_new      = str(e)
            self.whats_new_html = str(e)
            self.whats_new_md   = str(e)
            

    def need_to_upgrade(self):

        try:
            array  = self.latest.split('.')
            array1 = self.installed.split('.')

            (here_major, here_minor, here_pack, here_build) = (array1[0].strip(), array1[1].strip(), array1[2].strip(), array1[3].strip())            
            (site_major, site_minor, site_pack, site_build) = (array[0].strip(), array[1].strip(), array[2].strip(), array[3].strip())

            if here_major == site_major:
                if here_minor == site_minor:
                    if here_pack == site_pack:
                        if here_build == site_build:
                            return 0 # no_need_to_upgrade
                        else:
                            return 1 # may_upgrade
                else:
                    return 2 # should_upgrade

            return 3 # must_upgrade 

        except Exception as e:
            return 0 # in case of error we ignore it

