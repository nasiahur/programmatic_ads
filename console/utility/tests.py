import platform

from django.test import TestCase
from diladele.memory import Memory, Swap
from diladele.version import Version
from diladele.settings import WEBSAFETY_VAR_DIR
from diladele.system import SystemInfo, Uptime, CommandDiskFree
from diladele.license import LicenseManager
from diladele.tldextract import *

class TestCommandDisk(TestCase):
    def test_disk(self):    
        (success, info) = CommandDiskFree().run(WEBSAFETY_VAR_DIR)
        if success:
	    disk = {
		'free'  : info['avail'],
		'used'  : info['used'],
		'total' : info['size'],
		'ratio' : info['ratio'].replace('%', '')
	    }
            print disk

        #self.assertEqual(ext.domain, "cnn")
        #self.assertEqual(ext.suffix, "com")

       
'''
class TestTldExtract(TestCase):
    def test_extraction(self):    
        ext = tldextract.extract('http://forums.news.cnn.com/')
        self.assertEqual(ext.domain, "cnn")
        self.assertEqual(ext.suffix, "com")
        
        ext = tldextract.extract('http://www.mail.company.co.uk/')
        self.assertEqual(ext.suffix, "co.uk")
        self.assertEqual(ext.domain, "company")
        
        ext = tldextract.extract('http://safe-browsing.google.com/')
        self.assertEqual(ext.suffix, "com")
        self.assertEqual(ext.domain, "google")

class TestMemorySwap(TestCase):

    def test_memory(self):
        v = Memory().get()
        if platform.system() == "Windows":
            self.assertEqual(v['total'], 0)
            self.assertEqual(v['used'], 0)
            self.assertEqual(v['free'], 0)
        else:
            self.assertEqual(v['total'] > 0, True)
            self.assertEqual(v['used'] > 0, True)
            self.assertEqual(v['free'] > 0, True)
        
    def test_swap(self):
        v = Swap().get()
        if platform.system() == "Windows":
            self.assertEqual(v['total'], 0)
            self.assertEqual(v['used'], 0)
            self.assertEqual(v['free'], 0)
        else:
            self.assertEqual(v['total'] > 0, True)
            self.assertEqual(v['used'] > 0, True)
            self.assertEqual(v['free'] > 0, True)
        
class TestVersion(TestCase):

    def test_version(self):
        v = Version()
        self.assertEqual(v.up_to_date(), False)
        self.assertEqual(len(v.installed) > 0, True)
        #self.assertEqual(len(v.latest) > 0, True)
        
class TestSystem(TestCase):
    def test_uptime(self):
        v = Uptime()
        self.assertEqual(len(v.get()) > 0, True)
        
    def test_sysinfo(self):
        v = SystemInfo()
        self.assertEqual(len(v.get_hostname()) > 0, True)
        self.assertEqual(len(v.get_arch()) > 0, True)
        self.assertEqual(len(v.get_pythonver()) > 0, True)

class TestLicense(TestCase):
    def test_license(self):
        d = LicenseManager().get()
        self.assertEqual(d['status'], 'trial')
        self.assertEqual(d['key'], '03-04-000493E0-01-02-07DF-0019-00049BE2')
        self.assertEqual(len(d['expires']) > 0, True)
'''
