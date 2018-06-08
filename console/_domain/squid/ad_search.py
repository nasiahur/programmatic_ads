import os
import ldap
import tempfile

#
#
#
from _domain.core import Paths, System
from _domain.utils import Command, JsonDumper

#
#
#
class ldap_group:

    def __init__(self, dn="", name="", desc=""):

        self.name = name
        self.dn   = dn
        self.desc = desc
        
class ldap_user:
	
    def __init__(self, dn="", name="", sAMAccountName="", userPrincipalName=""):

        self.name = name
        self.dn   = dn
        self.sAMAccountName = sAMAccountName
        self.userPrincipalName = userPrincipalName
        
        
#
#
#
class LdapSearch:    

    def __init__(self, dc_addr, port, use_ldaps, base_dn, bind_user, bind_pass):

        # set size limit
        self.size_limit = 150

        # we do not support referrals
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        ldap.set_option(ldap.OPT_SIZELIMIT, self.size_limit)

        # set schema
        schema = "ldap"
        if use_ldaps:
            schema = "ldaps"

            # it is ldapS so set the path to the trusted cert
            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, os.path.join(Paths.etc_dir(), "ldaps.pem"))

            # disable certificate checking only on windows to ease development
            if System.name() == System.WS_WINDOWS:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            
        # construct uri
        uri = "%s://%s:%d" % (schema, dc_addr, port)

        # init LDAP and bind to it
        self.conn = ldap.initialize(uri)

        # bind to LDAP server
        self.conn.simple_bind_s(bind_user, bind_pass)

        # and save the base dn
        self.base_dn = base_dn

    def find_groups(self, name_contains = ""):

        # construct search filter
        filter = ""
        if len(name_contains) > 0:
            filter = "(&(objectClass=group)(groupType:1.2.840.113556.1.4.803:=2147483648)(name=*%s*))" % ldap.filter.escape_filter_chars(name_contains)
        else:
            filter = "(&(objectClass=group)(groupType:1.2.840.113556.1.4.803:=2147483648))"
            
        # define attributes to read
        attrs = ["dn", "name", "description"]

        # declare result
        result = []

        # run async search
        try:
            msgid = self.conn.search_ext(self.base_dn, ldap.SCOPE_SUBTREE, filter, attrs, sizelimit=self.size_limit)
            
            while True:
                (res_type, res_data) = self.conn.result(msgid, all=0)

                # have we reached the end
                if len(res_data) == 0:
                    break;
                        
                if res_type == ldap.RES_SEARCH_ENTRY:

                    # as we are passing all=0, res_data contains exactly one element
                    (dn, values) = res_data[0]

                    # create the group
                    g = ldap_group(dn)

                    if "name" in values and len(values["name"]) >= 1:
                        g.name = values["name"][0]

                    if "description" in values and len(values["description"]) >= 1:
                        g.desc = values["description"][0]

                    # and add it
                    result.append(g)

        except ldap.SIZELIMIT_EXCEEDED, e:
            pass

        # and return
        return result
        
    #
    # 
    #
    def find_users(self, base_dn, name_contains = ""):

        # construct search filter
        filter = ""
        if len(name_contains) > 0:
            filter = "(&(objectCategory=person)(objectClass=user)(name=*%s*))" % name_contains
        else:
            filter = "(&(objectCategory=person)(objectClass=user))"
        
        # (!userAccountControl:1.2.840.113556.1.4.803:=2) - not supported???
            
        # define attributes to read
        attrs = ["name", "dn", "sAMAccountName", "userPrincipalName"]

        # declare result
        result = []

        # run async search
        try:
            msgid = self.conn.search_ext(base_dn, ldap.SCOPE_SUBTREE, filter, attrs, sizelimit=self.size_limit)
            
            while True:
                (res_type, res_data) = self.conn.result(msgid, all=0)

                # have we reached the end
                if len(res_data) == 0:
                    break;
                        
                if res_type == ldap.RES_SEARCH_ENTRY:

                    # as we are passing all=0, res_data contains exactly one element
                    (dn, values) = res_data[0]

                    # create the user
                    u = ldap_user(dn)

                    if "name" in values and len(values["name"]) >= 1:
                        u.name = values["name"][0]

                    if "sAMAccountName" in values and len(values["sAMAccountName"]) >= 1:
                        u.sAMAccountName = values["sAMAccountName"][0]
                        
                    if "userPrincipalName" in values and len(values["userPrincipalName"]) >= 1:
                        u.userPrincipalName = values["userPrincipalName"][0]

                    # and add it
                    result.append(u)

        except ldap.SIZELIMIT_EXCEEDED, e:
            pass

        return result

    #
    #
    #
    def find_attributes(self, base_dn, user, attrs):

        # construct search filter
        filter = "(&(objectCategory=person)(objectClass=user)(name=*%s*))" % user

        # run async search
        try:
            msgid = self.conn.search_ext(base_dn, ldap.SCOPE_SUBTREE, filter, attrs, sizelimit=self.size_limit)

            while True:
                (res_type, res_data) = self.conn.result(msgid, all=0)

                # have we reached the end
                if len(res_data) == 0:
                    break;
                        
                if res_type == ldap.RES_SEARCH_ENTRY:

                    # as we are passing all=0, res_data contains exactly one element
                    (dn, values) = res_data[0]

                    # return the found attributes
                    return values

        except ldap.SIZELIMIT_EXCEEDED, e:
            pass
            
        # nothing found
        return {}
        
            
#
#
#
class LdapGroupSearcher:

    def __init__(self, dc_addr, port, use_ldaps, base_dn, bind_user, bind_pass):

        self.dc_addr   = dc_addr
        self.port      = port
        self.use_ldaps = use_ldaps
        self.base_dn   = base_dn
        self.bind_user = bind_user
        self.bind_pass = bind_pass

    def find_groups(self, pattern):

        try:
            value = []
            if len(pattern) > 0:

                # create the searcher
                s = LdapSearch(
                    self.dc_addr, 
                    self.port, 
                    self.use_ldaps,
                    self.base_dn,
                    self.bind_user,
                    self.bind_pass
                )

                value = s.find_groups(pattern)

            # and do the search            
            return { 'result' : True, 'error' : '', 'list' : value }

        except Exception as e:
            return { 'result' : False, 'error' : str(e), 'list' : [] }
            
            
#
# a wrapper for LDAP user search in group command
#
class CommandSearchLDAP(Command):

    def run(self, file):

        name = "ldap"
        if System.name() == System.WS_WINDOWS:
            name += ".exe"
    
        args = [os.path.join(Paths.bin_dir(), name), "--file=" + file]    
        
        # run this command
        (exit_code, stdout, stderr) = Command.run(self, args) 

        # and convert
        return { 'exit_code' : exit_code, 'stdout' : stdout, 'stderr' : stderr }
            
#
#
#
class LdapUserSearcher:

    def __init__(self, domain):
        self.domain = domain
        
    def find_user(self, groups, user):
    
        path = ""
        
        try:
            data = {
                'user'   : user,
                'groups' : []
            }
            for group in groups:
                data['groups'].append({ 'name' : group.name, 'dn': group.dn, 'recursive' : group.recursive})

            fout, path = tempfile.mkstemp()
            with os.fdopen(fout, 'w') as f:
                f.write(JsonDumper().dumps(data))

            # run search command
            data = CommandSearchLDAP().run(path)
            if data['exit_code'] == 0:
                return { 'result' : True,  'error' : '', 'output' : self.serialize(data) }
            
            raise Exception("%s" % self.serialize(data))
            
        except Exception as e:
            return { 'result' : False, 'error' : str(e) }
        finally:
            if len(path) > 0:
                os.unlink(path)
                
    def serialize(self, data):
        return "Exit Code: %d\nSTDOUT:\n%s\nSTDERR:\n%s" % (data['exit_code'], data['stdout'], data['stderr'])
