#!/usr/bin/env python
#
# (c) Diladele B.V. 2017, Web Safety for Squid Proxy
#  
import os
import sys
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
from frame.models import Profile
    
#
#
#
def generate():

    profile = Profile()
    profile.generate()

#
# main
#
def main():
    
    # define arguments
    parser = argparse.ArgumentParser(description='Generator of /opt/websafety/etc JSON configuration files. Warning: run as "sudo -u websafety generator.py" to get correct file permissions and owner.')
    
    # parse them (none but anyway)
    args = parser.parse_args()    

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)   
        
    # add domain
    generate()

    logging.info("Generator finished successfully. Please run /opt/websafety/bin/restart.sh or /opt/websafety/bin/reload.sh as desired!")
        
if __name__ == '__main__':

    main()