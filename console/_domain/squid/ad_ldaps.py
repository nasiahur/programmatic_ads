import os
import ssl

#
#
#
from _domain.core import Paths
from _domain.utils import Command

#
#
#
from binary_openssl import BinaryOpenSsl

#
#
#
class LdapsDetector:

    def __init__(self):

        self.exe = BinaryOpenSsl.full_path()

    def dump(self, cacert):

        cacert_path = os.path.join(Paths.etc_dir(), cacert)
        if not os.path.isfile(cacert_path):
            raise Exception("File %s does not exist or is not accessible!" % cacert_path)

        args = [self.exe, "x509", "-in", cacert_path, "-text"]

        (exit_code, stdout, stderr) = Command().run(args)             
        if exit_code != 0:
            raise Exception("Cannot run command %s, error:\n%s" % (" ".join(args), stdout + stderr))

        # if everything is fine - return the cert contents        
        return "%s\n%s" % (stdout, stderr)

    def dump_raw(self, cacert):

        cacert_path = os.path.join(Paths.etc_dir(), cacert)
        if not os.path.isfile(cacert_path):
            raise Exception("File %s does not exist or is not accessible!" % cacert_path)

        with open(cacert_path, 'r') as fin:
            return fin.read()


    def dump_from_server(self, server_addr):
        return ssl.get_server_certificate((server_addr, 636))

    
#
# test some stuff
#

'''
if __name__ == "__main__":

    detector = LdapsDetector()
    try:
        detector.dump("ldaps.pem")
    except Exception as e:
        print str(e)

    try:
        data = detector.dump_from_server("192.168.1.3")
        print data
    except Exception as e:
        print str(e)
'''