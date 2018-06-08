import re
import ldap

#
# domain
#
from _domain.core import System
from _domain.utils import Command

#
# ours
#
from binary_klist import BinaryKlist
from binary_kinit import BinaryKinit
from ad_search    import LdapSearch

#
# 
#
class KeyTabDumper:

    def __init__(self):

        self.exe = BinaryKlist.full_path()

    def dump(self, keytab_path):

        if System.name() == System.WS_WINDOWS:
            return "Showing KEYTAB %s contents on windows ALWAYS SUCCEEDS with this message." % keytab_path

        if System.name() == System.WS_FREEBSD:
            return self.run_freebsd(keytab_path)
            
        return self.run_linux(keytab_path)

    def run_linux(self, keytab_path):

        args = [self.exe, "-k", "-K", "-t", "-e", keytab_path]

        (exit_code, stdout, stderr) = Command().run(args) 
        if exit_code != 0:
            raise Exception("Cannot run command %s, error:\n%s" % (" ".join(args), stdout + stderr))

        return stdout + "\n" + stderr

    def run_freebsd(self, keytab_path):

        args = [self.exe, "-v", "-k", keytab_path, "list"]

        (exit_code, stdout, stderr) = Command().run(args) 
        if exit_code != 0:
            raise Exception("Cannot run command %s, error:\n%s" % (" ".join(args), stdout + stderr))

        return stdout + "\n" + stderr

#
#
#
class KeyTabInitializer:

    def __init__(self):
        self.exe = BinaryKinit.full_path()

    def initialize(self, keytab_path, spn):
        
        try:
            if System.name() == System.WS_WINDOWS:
                return (True, "Trying actual key tab %s on Windows with SPN %s ALWAYS SUCCEEDS" % (keytab_path, spn))

            if System.name() == System.WS_FREEBSD:
                return (True, self.run_freebsd(keytab_path, spn))

            return (True, self.run_linux(keytab_path, spn))

        except Exception as e:
            return (False, str(e))


    def run_linux(self, keytab_path, spn):

        # now we should also call the actual kinit to see if it can connect to the domain
        args = [self.exe, "-V", "-k", "-t", keytab_path, spn]

        (exit_code, stdout, stderr) = Command().run(args) 
        if exit_code != 0:
            raise Exception("Cannot run command %s, error:\n%s" % (" ".join(args), stdout + stderr))

        return stdout + "\n" + stderr

    def run_freebsd(self, keytab_path, spn):

        # now we should also call the actual kinit to see if it can connect to the domain
        args = [self.exe, "-k", "-t", keytab_path, spn]

        (exit_code, stdout, stderr) = Command().run(args) 
        if exit_code != 0:
            raise Exception("Cannot run command %s, error:\n%s" % (" ".join(args), stdout + stderr))

        return stdout + "\n" + stderr


#
#
#
class KvnoRetriever:

    def __init__(self, dc_addr, port, use_ldaps, base_dn, bind_user, bind_pass):

        self.dc_addr   = dc_addr
        self.port      = port
        self.use_ldaps = use_ldaps
        self.base_dn   = base_dn
        self.bind_user = bind_user
        self.bind_pass = bind_pass

    def retrieve(self):

        # create the searcher
        s = LdapSearch(
            self.dc_addr, 
            self.port, 
            self.use_ldaps,
            self.base_dn,
            self.bind_user,
            self.bind_pass
        )

        attributes = s.find_attributes(self.base_dn, self.bind_user, ["objectClass", "name", "msDS-KeyVersionNumber", "canonicalName" ])

        # see if the KVNO is there
        if "msDS-KeyVersionNumber" not in attributes:
            raise Exception("Cannot find msDS-KeyVersionNumber attribute in LDAP search result %s" % attributes)

        kvnos = attributes["msDS-KeyVersionNumber"]
        if len(kvnos) != 1:
            raise Exception("Kvno array length is not 1 in LDAP search result %s" % attributes)
        knvno = kvnos[0]

        # return as string
        return str(knvno)

#
# kvno checker compares the KVNO from passed in keytab with KVNO from LDAP
#
class KvnoChecker:

    def __init__(self, dc_addr, port, use_ldaps, base_dn, bind_user, bind_pass):

        self.dc_addr   = dc_addr
        self.port      = port
        self.use_ldaps = use_ldaps
        self.base_dn   = base_dn
        self.bind_user = bind_user
        self.bind_pass = bind_pass

    def check(self, keytab_path, keytab_spn):
        
        try:
            if not self.dc_addr:
                raise Exception("No LDAP server address specified, KVNO check is not possible!")

            # get kvno from LDAP
            kvno_ldap = KvnoRetriever(self.dc_addr, self.port, self.use_ldaps, self.base_dn, self.bind_user, self.bind_pass).retrieve()

            # get kvno from KEYTAB
            kvno_keytab = self.get_keytab_kvno(keytab_path, keytab_spn)

            # prepare message
            msg = "KVNO stored in LDAP server '%s' is %s and KVNO stored in keytab '%s' is %s" % (self.dc_addr, kvno_ldap, keytab_path, kvno_keytab)

            # compare them
            if kvno_ldap != kvno_keytab:
                raise Exception("Kerberos authentication may NOT work correctly. Error: KNVO NOT EQUAL - %s!" % msg)

            return (True, "SUCCESS: %s" % msg)

        except Exception as e:
            return (False, str(e))


    def get_keytab_kvno(self, keytab_path, keytab_spn):

        if not keytab_spn:
            raise Exception("Cannot determine KVNO in keytab '%s' without SPN! Please specify SPN first and then retry." % keytab_path)

        records = []
        dumped  = KeyTabDumper().dump(keytab_path).split('\n')
        for line in dumped:
            
            smatch = re.match( r'\s*(\d+)\s(\d\d\/\d\d\/\d\d)\s+(\d\d:\d\d:\d\d)\s+(HTTP\/\S+@\S+)\s+.*$', line, re.M|re.I)
            if smatch:
                kvno = smatch.group(1)
                date = smatch.group(2)
                time = smatch.group(3)
                spn  = smatch.group(4)

                if spn == keytab_spn:
                    return kvno

        return None
    