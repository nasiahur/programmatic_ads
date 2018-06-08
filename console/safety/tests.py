from django.test import TestCase

'''
from django.contrib.auth import authenticate

from qlproxy.ldap_server import LdapDetector, LdapGroupSearcher, LdapUserSearcher
from qlproxy.categories import DomainCategorizer
from qlproxy.history import HistoryManager
from qlproxy.models import SurfingNow, Ldap, MemberLdap


class TestLdapSearch(TestCase):

    def get_ldap_info(self):
        info = Ldap()
        info.server   = "172.16.1.216"
        info.schema   = Ldap.SCHEMA_LDAP
        info.port     = 389
        info.binduser = "Administrator@example.lan"
        info.bindpass = "Passw0rd"
        info.basedn   = "dc=example,dc=lan"
        return info
    
    def test_group_search(self):    
        info = self.get_ldap_info()
        
        s = LdapGroupSearcher()
        r = s.find_groups(info, "internet")
        self.assertEqual(r['result'], True)
        self.assertEqual(len(r['list'])>0, True)
        
    def test_user_search(self):    
        s = LdapUserSearcher(self.get_ldap_info())
        
        g = MemberLdap()
        g.dn = "cn=Internet Strict,cn=Users,dc=example,dc=lan"
        g.recursive = True
    
        r = s.find_user(g, "john.rambo@example.lan")
        if not r['result']:
            print r['error']
            
        self.assertEqual(r['result'], True)
        
        

'''
#
#
#

'''
class TestHistory(TestCase):
    
    def test_1(self):    
        c = HistoryManager().get_raw()
        
        if c['success'] == True:
            self.assertEqual(len(c['error']) == 0, True)
            for event in c['events']:
                pass
        else:
            self.assertEqual(c['success'], False)
            self.assertEqual(len(c['error']) > 0, True)
            self.assertEqual(c['events'], [])
            
    def test_invalid_group_by(self):    
        f = SurfingNow()
        f.filter = "google.com"
        c = HistoryManager()
        
        self.assertRaises(Exception, c.get, f)
        
    def test_group1(self):    
        f = SurfingNow()
        f.filter   = "google.com"
        f.group_by = SurfingNow.GROUP_BY_IP
        c = HistoryManager()        
        d = c.get(f)
        for key in d.keys():
            print key
            for value in d[key]:
                print "\t" + value.host2
                        
            
        
        
        
            
            
        

#
#
# 
class TestCategorizer(TestCase):
    
    def test_outlook(self):
        data = DomainCategorizer().categorize("outlook.com")
        self.assertEqual(data[0], 'webmail')
        
    def test_facebook(self):
        data = DomainCategorizer().categorize("facebook.com")
        self.assertEqual(data[0], 'social_networking')
        
    def test_empty(self):
        data = DomainCategorizer().categorize("")
        self.assertEqual(data, [])
        
#
#
#
class TestLdap(TestCase):
    
    def test_generator(self):
        data = LdapDetector().detect()
        
        self.assertEqual(len(data['server']), 0)
        self.assertEqual(data['port'], 389)
        self.assertEqual(len(data['basedn']), 0)
        self.assertEqual(len(data['binduser']), 0)
'''