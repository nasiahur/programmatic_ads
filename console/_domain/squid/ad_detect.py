import socket
#
#
#
from ad_realm import RealmDetector
from ad_ldap  import LdapDetector

#
#
#
class AdDetector:

    def detect(self):
        
        # detect realm
        realm = RealmDetector().detect()

        # now detect the ldap domain controllers
        info = LdapDetector().detect()    
        data = [{
            'error' : False,
            'info'  : {
                'realm'  : realm,
                'spn'    : "HTTP/%s@%s" % (socket.getfqdn().lower(), realm),
                'dc1addr': info['server1'],
                'dc2addr': info['server2'],
                'rootdn' : info['basedn']
            }
        }]
        
        # and return
        return data

#
# test some stuff
#
#if __name__ == "__main__":
#
#    print "AdDetector::detect() == %s" % AdDetector().detect()
#    