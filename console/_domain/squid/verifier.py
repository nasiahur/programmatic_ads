import os
import re
import tempfile


#
#
#
from _domain.core import System

#
#
#
from binary_openssl import BinaryOpenSsl

#
# in order to verify certificates we dump first one to site.pem and all others as intermediateN.pem into -untrusted
#
class CertChainVerifier:

    def __init__(self, server_name):

        self.server_name = server_name

    def verify(self, certs):

        # check we have at least leaf
        if not certs:
            raise Exception("Input chain of certificates MUST contain at least one certificate to verify")

        # split the chain into leaf and untrusted certificates
        (leaf, untrusted) = self.split_chain(certs)

        # dump those into two temp files
        (path_leaf, path_untrusted) = self.dump_certs(leaf, untrusted)

        # for debug
        leave_files_for_debug = False

        try:

            # will throw in case if bad certs
            self.verify_openssl(path_leaf, path_untrusted)

            # certificates may be fine; but we also need to verify the hostname name - see https://wiki.openssl.org/index.php/Hostname_validation
            self.verify_hostname(self.server_name, certs)
        
        except Exception as e:
            
            # verification failed
            return (False, str(e))

        finally:

            if not leave_files_for_debug:

                # remove leaf
                if os.path.isfile(path_leaf):
                    os.unlink(path_leaf)

                # remove untrusted
                if os.path.isfile(path_untrusted):
                    os.unlink(path_untrusted)


        # if we got here everything is fine
        return (True, "")

    def split_chain(self, certs):

        leaf      = ""
        untrusted = []

        first = True
        for cert in certs:
            if first:
                leaf  = cert.pem
                first = False
            else:
                untrusted.append(cert.pem)

        return (leaf, untrusted)

    def dump_certs(self, leaf, untrusted):

        # dump leaf
        path_leaf = self.dump_cert(leaf, "leaf")

        # assume no untrusted at all
        path_untrusted = ""

        # see if we have untrusted
        if len(untrusted) > 0:

            # first cat the untrusted together
            combined = "\n".join(untrusted)

            # dump untrusted
            path_untrusted = self.dump_cert(combined, "untrusted")

        return (path_leaf, path_untrusted)

    def dump_cert(self, cert, suffix):

        # write to temp file        
        with tempfile.NamedTemporaryFile(prefix="websafety_ssl_server_test.%s." % suffix, dir=tempfile.gettempdir(), delete=False) as temp:

            temp.write(cert)
            temp.flush() 

        return temp.name

    def get_ca_arg(self):

        # for debug
        if System.name() == System.WS_WINDOWS:
            return "-CAfile C:\\OpenSSL-Win32\\bin\\ca-certificates.crt"

        # see if this is ubuntu/debian
        if os.path.isdir("/etc/ssl/certs"):
            return "-CApath /etc/ssl/certs"

        # see if this is centos
        if os.path.isfile("/etc/pki/tls/certs/ca-bundle.crt"):
            return "-CAfile /etc/pki/tls/certs/ca-bundle.crt"

        # then it must be freebsd
        if os.path.isfile("/etc/ssl/cert.pem"):
            return "-CAfile /etc/ssl/cert.pem"

        raise Exception("Cannot determine location for CApath or CAfile!")

    def verify_openssl(self, path_leaf, path_untrusted):

        # this is the output file to capture stdout and stderr from openssl
        output_file = ""

        # make it
        with tempfile.NamedTemporaryFile(prefix="websafety_ssl_server_test.output.", dir=tempfile.gettempdir(), delete=False) as temp:
            output_file = temp.name

        # we need this to utilize finally
        leave_files_for_debug = False

        try:
            args = "verify %s" % self.get_ca_arg()
            if path_untrusted != "":
                args += " -untrusted %s" % path_untrusted
            args += " %s" % path_leaf

            # run openssl
            openssl_exe = BinaryOpenSsl.full_path()
            command     = "%s %s >%s 2>&1" % (openssl_exe, args, output_file)
            exit_code   = os.system(command)
            
            if exit_code != 0:

                # read contents of output file
                output = ""
                if os.path.isfile(output_file):

                    with open(output_file, "r") as fin:
                        output = fin.read()
                        output = output.replace("\n", " ")

                # and throw
                raise Exception("Failed to run: %s; STDOUT: %s" % (command, output))

        finally:

            if not leave_files_for_debug:
                if os.path.isfile(output_file):
                    os.unlink(output_file)

    def verify_hostname(self, server_name, certs):

        #
        # see https://wiki.openssl.org/index.php/Hostname_validation
        #
        assert(server_name)
        assert(len(certs) > 0)

        # get the leaf cert
        leaf = certs[0]

        # get alternative names
        valid = HostNameVerifier().verify(server_name, leaf)
        if not valid:
            raise Exception("Cannot match server name '%s' with provided site certificate." % server_name)

#
#
#
class HostNameVerifier:

    def verify(self, server_name, cert):

        # first we need to verify the alternative names
        names = self.get_alt_names(cert)
        for name in names:
            if self.match(name, server_name):
                return True

        # ok then we need to verify the common name
        common_name = self.get_common_name(cert)

        # and return either true or false
        return self.match(common_name, server_name)

    def get_alt_names(self, cert):

        result = []

        value = cert.subjectAltNames()
        items = value.split(",")
        for item in items:

            item = item.strip()
            if item.startswith("DNS:"):
                dns = item[4:].strip()
                if len(dns) > 0:
                    result.append(dns)

        return result

    def get_common_name(self, cert):
        return cert.x509.get_subject().commonName

    def match(self, name, server_name):

        pattern = name
        pattern = pattern.replace(".", "\\.")
        pattern = pattern.replace("*", ".*")

        result = re.match(pattern, server_name)
        if result:
            return True

        return False

