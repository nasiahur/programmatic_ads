import json
import urllib2

#
#
#
class ClusterServerNodesList:

    def run(self, wsmgrd_port):

        # this is the data returned by wsmgrd
        data = ""

        # try to get data from wsmgrd
        url  = "http://127.0.0.1:%d/cluster/nodes" % wsmgrd_port                        
        resp = urllib2.urlopen(url)
        data = resp.read()
        
        # convert list to json
        return json.loads(data)