#!/usr/bin/env python
#
# (c) Diladele B.V. 2017, Web Safety for Squid Proxy
#  
# Upgrades (imports) configuration settings from previous versions. Should be run manually.
#
import os
import re
import sys
import json
import django
import logging
import argparse

#
# in order for Django to work correctly with our monitor app, we add ourselves to Python's search path
# 
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
from django.db.models import Max
from frame.models import Upgrader

         
#
# main
#
def main():
    
    # define arguments
    parser = argparse.ArgumentParser(description='Upgrades configuration settings from previous version')
    parser.add_argument("--etc_dir", help="full path to a copy of /opt/websafety/etc folder from previous version", required=True)
    parser.add_argument("--version", help="version to upgrade from (for example, 5.0, 5.1 or 5.2)", required=True)
    parser.add_argument("--test",    help="do not actually import, just test if it would work", required=False, default=False, action='store_true')
    
    # parse them
    args = parser.parse_args()    

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)   
        
    # do the upgrade
    upgrader = Upgrader(args.test, args.version)
    upgrader.upgrade(args.etc_dir)

    logging.info("All settings from previous version imported successfully. Please login into Web UI and check if everything is ok!")
        
if __name__ == '__main__':

    main()