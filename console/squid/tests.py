from django.test import TestCase

# Create your tests here.
from squid.models import *

class TestSquid(TestCase):

    def test_1(self):    
        squid = Squid()
        self.assertEqual(squid.icap_user_ip_available(), True)
        self.assertEqual(squid.icap_user_name_available(), True)