#
#
#
import os
import socket

#
#
#
class RealmReader:

    def read(self):

        r1 = self.from_resolv_conf()
        r2 = self.from_socket()
        
        if len(r1) == 0:
            return r2
        elif r1.find(".") == -1:
            if len(r2) == 0:
                return r1
            else:
                return r2
        else:
            return r1

    def from_socket(self):

        # ask system name as FQDN
        value0 = socket.getfqdn()
        
        # see if there is a . in the system name
        value1 = value0
        pos    = value1.find(".")
        if pos != -1:
            value1 = value1[pos + 1:]

        # see if there is a dot in the rest
        if value1.find(".") == -1:

            # no dot, then just return the original value
            return value0.upper()

        # otherwise return chomped value
        return value1.upper()

    def from_resolv_conf(self):
        result = ""
        if os.path.isfile("/etc/resolv.conf"):
            fin = open("/etc/resolv.conf")
            for line in fin.readlines():
                if not line.strip().startswith('#'):
                    array = line.strip().split(' ')
                    if array[0] == "search":
                        result = array[1]
                        break        
        
        return result.upper()

#
#
#
class RealmDetector:

    def detect(self):

        reader = RealmReader()        
        realm  = reader.read()
        if realm:
            return realm

        return "UNKNOWN"


#
# test some stuff
#

'''
if __name__ == "__main__":

    print "RealmReader::read()     => %s" % RealmReader().read()
    print "RealmDetector::detect() => %s" % RealmDetector().detect()
'''