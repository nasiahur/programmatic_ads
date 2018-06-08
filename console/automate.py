#!/usr/bin/env python
#
# (c) Diladele B.V. 2018, Web Safety for Squid Proxy
#  
# Sample automation script
#
import os
import sys
import django
import logging
import argparse

#
# in order for Django to work correctly with our monitor app, we add ourselves
# to Python's search path
sys.path.append(os.path.abspath(__file__))

#
# tell Django where to read settings from
#
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "console.settings")

#
#
#
django.setup()

#
# do imports
#
from safety.models import *
from squid.models import *
    
#
#
#
def add_domain(domain):

    item = None
    try:
        item = ExcludeDomainName.objects.get(value=domain)
    except ExcludeDomainName.DoesNotExist:        
        item = ExcludeDomainName(value=domain)

    item.comment = "Some comment!"
    item.save()

#
# main
#
def main():
    
    # define arguments
    parser = argparse.ArgumentParser(description='Automation sample for Web Safety')
    parser.add_argument("--domain", help="name of the domain to exclude from HTTPS decryption", required=True)

    # parse them
    args = parser.parse_args()    

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)   
        
    # add domain
    add_domain(args.domain)

    logging.info("Domain %s added successfully. Please login into Web UI and check if everything is ok!" % args.domain)
        
if __name__ == '__main__':

    main()