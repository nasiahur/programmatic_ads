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
# inspects RootDSE in the given server (anonymous bind)
#
class LdapRootDSE:

    def inspect(self, server_addr):

        if len(server_addr) == 0:
            return ("", "")

        return self.bind_and_inspect(server_addr)

    def bind_and_inspect(self, server_addr):

        defaultNamingContext = ""
        currentTime          = ""

        try:

            uri  = "ldap://%s:389" % server_addr
            conn = ldap.initialize(uri)

            # we bind anonymously which is allowed for the RootDSE only
            conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 7.0)
            conn.simple_bind_s('', '')

            # do the search
            entries = conn.search_s("", ldap.SCOPE_BASE, "objectclass=*", None)
            for (dn, attrs) in entries:                
                for key, value in attrs.iteritems():
                    if key == "defaultNamingContext":
                        defaultNamingContext = value[0]
                    if key == "currentTime":
                        currentTime = value[0]

        except Exception as e:
            pass

        return (defaultNamingContext, currentTime)


#
# test some stuff
#

'''
if __name__ == "__main__":

    print "LdapRootDSE::inspect() == %s" % str(LdapRootDSE().inspect("192.168.1.3"))
    print "LdapRootDSE::inspect() == %s" % str(LdapRootDSE().inspect("192.168.1.4"))
'''