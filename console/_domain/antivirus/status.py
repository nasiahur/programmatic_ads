import json
import urllib2

class WsGsbStatus(object):

    def run(self, port):

        # this is the data returned by wsgsbd
        data = ""

        # try to get data from wsmgrd
        url  = "http://127.0.0.1:%d/status" % port                        
        resp = urllib2.urlopen(url)
        data = resp.read()
        
        # convert response to json
        return json.loads(data)