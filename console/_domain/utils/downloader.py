import urllib2
import platform

#
#
#
class FileDownloader:

    def __init__(self, version, arch):

        self.version = version
        self.arch    = arch
        
    def download_file(self, url):
        
        user_agent = "Diladele Web Safety for Squid Proxy Web UI/%s/%s (%s)" % (self.version, self.arch, platform.platform())
        headers    = { 'User-Agent' : user_agent }        
        req        = urllib2.Request(url, None, headers)
        resp       = urllib2.urlopen(req)        
        return resp.read()
        