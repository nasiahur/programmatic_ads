import os
import tempfile

from openssl_exe import OpenSslExe, OpenSslParser
from cert_factory import CertificateFactory


#
#
#
class CertChainCollector:

    def __init__(self, server_name, server_port=443):

        self.server_name = server_name
        self.server_port = server_port

    def collect(self):

        # this is the output file to capture stdout and stderr from openssl
        output_file = ""

        # make it
        with tempfile.NamedTemporaryFile(prefix="websafety_ssl_server_test.output.collector.", dir=tempfile.gettempdir(), delete=False) as temp:
            output_file = temp.name

        # we need this to utilize finally
        leave_files_for_debug = False

        try:
            # get the chain of certificates from the remove server
            data = OpenSslExe().run(self.server_name, self.server_port, output_file)

            # parse them into list of PEMs
            pems = OpenSslParser().parse(data)

            # create list of x509 objects
            certs = CertificateFactory().construct(pems)

            # verify the certificates as a whole
            return certs

        finally:

            if not leave_files_for_debug:
                if os.path.isfile(output_file):
                    os.unlink(output_file)