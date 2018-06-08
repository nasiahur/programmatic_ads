#
# system
#
import os
import json
import errno

#
# utils
#
from _domain.core import Paths
from _domain.utils import Command, CommandElevated

#
#
#
from binary_certmgr import BinaryCertMgr

#
#
#
class SquidCertDumper:

    def __init__(self):

        self.exe = BinaryCertMgr.full_path()

    def as_json(self, pem):

        arg1 = "--action=verify-root-certificate"
        arg2 = "--input=" + pem
        args = [self.exe, arg1, arg2]

        # get the certificate info        
        (exit_code, stdout, stderr) = Command().run(args)
        if exit_code == 0:
            return json.loads(stdout)

        # if we got here everything is bad
        raise Exception(
            "Command %s failed.\n\tExit Code: %d\n\tSTDOUT: %s\n\tSTDERR: %s" % (" ".join(args), exit_code, stdout, stderr)
        )

#
#
#
class SquidCertConverter:

    def __init__(self):

        self.exe = BinaryCertMgr.full_path()

    def to_der(self, pem, der):

        # run the certificate convert tool
        arg1 = "--action=convert-root-certificate"
        arg2 = "--input=" + pem
        arg3 = "--output=" + der
        args = [self.exe, arg1, arg2, arg3]

        (exit_code, stdout, stderr) = Command().run(args)
        if exit_code == 0:
            return

        # if we got here everything is bad
        raise Exception(
            "Command %s failed.\n\tExit Code: %d\n\tSTDOUT: %s\n\tSTDERR: %s" % (" ".join(args), exit_code, stdout, stderr)
        )

#
# 
#
class SquidCertDbInitializer:

    def __init__(self):

        self.exe = BinaryCertMgr.full_path()
    
    def initialize(self):   

        arg  = "--action=regenerate-certificate-storage"
        args = [self.exe, arg]

        (exit_code, stdout, stderr) = CommandElevated().run(args)
        if exit_code == 0:
            return

        # if we got here everything is bad
        raise Exception(
            "Command %s failed.\n\tExit Code: %d\n\tSTDOUT: %s\n\tSTDERR: %s" % (" ".join(args), exit_code, stdout, stderr)
        )

#
# 
#
class SquidCertGenerator:

    def __init__(self):

        self.exe = BinaryCertMgr.full_path()

    def generate(self, path_to_cert_pem, country, state, city, organization, ou, email, cn, days):   

        # create arguments array
        data = {
            'country'             : country,
            'province'            : state,
            'city'                : city,
            'organization'        : organization,
            'organizational-unit' : ou,
            'common-name'         : cn,
            'e-mail'              : email,
            'lifetime'            : days,
            'output'              : path_to_cert_pem
        }
        args = [self.exe, "--action=create-root-certificate"]
        for key in data.keys():
            args.append("--%s=%s" % (key, str(data[key])))

        (exit_code, stdout, stderr) = Command().run(args)
        if exit_code == 0:
            return

        # if we got here everything is bad
        raise Exception(
            "Command %s failed.\n\tExit Code: %d\n\tSTDOUT: %s\n\tSTDERR: %s" % (" ".join(args), exit_code, stdout, stderr)
        )

#
#
#
class SquidCert:

    def __init__(self):

        self.pem_path = os.path.join(Paths.etc_dir(), "myca.pem")
        self.der_path = os.path.join(Paths.etc_dir(), "myca.der")

    def get(self):
        return SquidCertDumper().as_json(self.pem_path)

    def upload(self, data):

        # first we try to write the file next to actual one
        cur_pem = self.pem_path
        new_pem = cur_pem + ".new"
        cur_der = self.der_path
        new_der = cur_der + ".new"

        # remove the existing new file(s) which may not even exist
        try:
            os.remove(new_pem)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        try:
            os.remove(new_der)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        # write the new pem file 
        with open(new_pem, 'wb') as fout:
            for chunk in data.chunks():
                fout.write(chunk)

        # dump the new pem and thus verify it
        cert = SquidCertDumper().as_json(new_pem)

        # see if this certificate IS root ca
        if not cert['IsCA']:
            raise Exception("The file '%s' does not contain a Root CA certificate, Squid cannot used such PEM file for SSL decryption" % new_pem)

        # ok file is good; now we need to convert it to DER
        SquidCertConverter().to_der(new_pem, new_der)
        
        # now replace the new files 
        if os.path.isfile(cur_pem):
            os.remove(cur_pem)
        if os.path.isfile(cur_der):
            os.remove(cur_der)
        
        os.rename(new_pem, cur_pem)
        os.rename(new_der, cur_der)

        # perfect now reinitialize the SSL storage (ensure you have the right to write into squid folder!)
        SquidCertDbInitializer().initialize()

    def generate(self, country, state, city, organization, ou, email, cn, days):

        # first we try to write the file next to actual one
        cur_pem = os.path.join(Paths.etc_dir(), "myca.pem")
        new_pem = cur_pem + ".new"
        cur_der = os.path.join(Paths.etc_dir(), "myca.der")
        new_der = cur_der + ".new"
                
        # remove the existing new file(s) which may not even exist
        try:
            os.remove(new_pem)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        try:
            os.remove(new_der)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        # generate the new pem file by calling special command
        SquidCertGenerator().generate(new_pem, country, state, city, organization, ou, email, cn, days)
        
        # ok file is good; now we need to convert it to DER
        SquidCertConverter().to_der(new_pem, new_der)

        # replace the new files 
        if os.path.isfile(cur_pem):
            os.remove(cur_pem)
        if os.path.isfile(cur_der):
            os.remove(cur_der)
        
        os.rename(new_pem, cur_pem)
        os.rename(new_der, cur_der)

        # perfect now reinitialize the SSL storage (ensure you have the right to write into squid folder!)
        SquidCertDbInitializer().initialize()

