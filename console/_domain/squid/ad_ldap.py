# note on windows get a package from http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap
# and install it like
#
#   cd c:\Python27\Scripts
#   pip install python_ldap-2.4.25-cp27-none-win32.whl
#
try:
    import ldap
    import ldap.filter
except:
    pass

#
#
#
from ad_dns import DnsDigger
from ad_realm import RealmReader
from ad_rootdse import LdapRootDSE


#
#
#
class LdapDetector:

    def __init__(self):

        # reset the members
        self.clear()

    def clear(self):

        # reset the members
        self.realm    = ""
        self.basedn   = ""
        self.binduser = ""
        self.server1  = ""
        self.server2  = ""

    def collect_realm(self):

        # assign realm
        self.realm = RealmReader().read()

        # and predefined user name
        self.binduser = "squid@%s" % self.realm.lower()
        
    def collect_servers(self):

        # construct ldap server dns name
        name = "_ldap._tcp.%s" % self.realm.lower()
        name = name.lower()

        # make DNS query to using dig 
        servers = DnsDigger().dig(name)
        if len(servers) == 0:

            # no servers at all
            return

        if len(servers) == 1:

            # only one server, see its host and port
            (s0, p0) = servers[0]

            # and assign
            self.server1 = s0

        if len(servers) > 1:

            # two or more servers, get only two
            (s0, p0) = servers[0]
            (s1, p1) = servers[1]

            # and assign
            self.server1 = s0
            self.server2 = s1

    def collect_rest(self):

        # these are local copies of two servers
        s0 = self.server1
        s1 = self.server2

        # inspect both servers
        (d0, c0) = LdapRootDSE().inspect(s0)
        (d1, c1) = LdapRootDSE().inspect(s1)

        # all of d0, c0, d1, c1 may be empty, when for example the domain controllers are switched off
        if not d0 or not c0:
            s0 = ""
        if not d1 or not c1:
            s1 = ""

        # check the servers
        if not s0 and not s1:

            # we could not get information from any server, construct predefined value based on the dn
            self.basedn  = "dc=" + ',dc='.join(self.realm.lower().split('.'))
            self.curtime = ""

        if s0:

            # the first server replied, assign the values
            self.basedn  = d0
            self.curtime = c0

            # and move it up
            self.server1 = s0
            self.server2 = s1

        if s1:

            # the second server replied, assign the values
            self.basedn  = d1
            self.curtime = c1

            # and move it up
            self.server1 = s1
            self.server2 = s0

    def detect(self):

        # reset the members
        self.clear()

        # fill all members
        self.collect_realm()
        self.collect_servers()
        self.collect_rest()

        # assign and return
        data = {
            'basedn'  : self.basedn, 
            'binduser': self.binduser,
            'server1' : self.server1,
            'server2' : self.server2,
            'curtime' : self.curtime
        }

        # and return
        return data

    def inspect_rootdse(self, server_addr):

        defaultNamingContext = ""
        currentTime          = ""

        if len(server_addr) > 0:
            
            # try to anonymously bind to RootDSE
            try:
                uri  = "ldap://%s:389" % server_addr
                conn = ldap.initialize(uri)

                # we bind anonymously which is allowed for the RootDSE only
                conn.simple_bind_s('', '')

                # do the search
                entries = conn.search_s("", ldap.SCOPE_BASE, "objectclass=*", None)
                for (dn, attrs) in entries:                
                    for key, value in attrs.iteritems():
                        if key == "defaultNamingContext":
                            defaultNamingContext = value
                        if key == "currentTime":
                            currentTime = value

            except Exception as e:
                print (str(e))
                pass

        return (defaultNamingContext, currentTime)

    

#
# test some stuff
#
#if __name__ == "__main__":
#
#    print "LdapDetector::detect() =>"
#    print LdapDetector().detect()
