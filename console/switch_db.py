#!/usr/bin/env python
#
# (c) Diladele B.V. 2017, Web Safety for Squid Proxy
#  
# switch_db.py
#
import os
import sys
import time
import shutil
import logging
import argparse
import datetime

#
# in order for Django to work correctly with our monitor app, we add ourselves to Python's search path
# 
sys.path.append(os.path.abspath(__file__))

#
# tell Django where to read settings from
#
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "console.settings")

#
# do imports
#
from _domain.core import Paths, System
from _domain.utils import Command

#
#
#
from console.settings import WEBSAFETY_MONITOR_DB_MYSQL

#
# 
#
class CommandDatabase(Command):
    
    def run(self, params):   

        name = "database"
        if System.name() == System.WS_WINDOWS:
            name += ".exe"

        exe  = os.path.join(Paths.bin_dir(), name)
        args = [exe]
        args.extend(params)

        (exit_code, stdout, stderr) = Command.run(self, args)
        if exit_code != 0:
            logging.error("ERROR: ")
            logging.error("ERROR: Cannot switch database, error: %d", exit_code)
            logging.error("ERROR: ")

            logging.error("STDOUT: ")
            logging.error(stdout)

            logging.error("STDERR: ")
            logging.error(stderr)

            raise Exception("FAILURE!!!")
    
#
#
#
def switch_to_mysql():

    # first see if the flag is there
    flag = os.path.join(Paths.var_dir(), "console", "console", "database.mysql")
    if not os.path.exists(flag):

        logging.info("Current system uses SQLite as monitoring database (flag file %s does not exist)." % flag)
        logging.info("Adding flag to switch to MySQL...")

        with open(flag, "w") as fout:
            fout.write("Switches local monitoring database to MySQL (connection settings are in /opt/websafety/var/console/console/settings.py)")

        logging.info("Flag added successfully")
    else:
        logging.warning("Current system already uses MySQL as monitoring database (flag file %s exists)." % flag)
        logging.warning("Your current monitoring database will be reinitialized")

    # pass the MySQL settings as command line parameters to the database initializing script
    args = [
        "--db=mysql",
        "--host=%s" % WEBSAFETY_MONITOR_DB_MYSQL['HOST'],
        "--port=%d" % int(WEBSAFETY_MONITOR_DB_MYSQL['PORT']),
        "--user=%s" % WEBSAFETY_MONITOR_DB_MYSQL['USER'],
        "--pass=%s" % WEBSAFETY_MONITOR_DB_MYSQL['PASSWORD']
    ]
    
    # and generate
    CommandDatabase().run(args)
    

#
# 
#
def switch_to_sqlite():

    # first see if the flag is there
    flag = os.path.join(Paths.var_dir(), "console", "console", "database.mysql")
    if os.path.exists(flag):

        logging.info("Current system uses MySQL as monitoring database (flag file %s exists)." % flag)
        logging.info("Removing flag to switch to SQLite...")

        os.remove(flag)
        logging.info("Flag removed successfully")

    # now resetting the SQLite database to default state
    db_cur = os.path.join(Paths.var_dir(), "db", "monitor.sqlite")
    db_old = os.path.join(Paths.var_dir(), "db", "monitor.sqlite.old")
    db_def = os.path.join(Paths.var_dir(), "db", "monitor.sqlite.default")

    # see if the old database exists
    if os.path.exists(db_old):

        # yes, it is better to stop here and ask the user to remove it manually
        logging.error("Old version of database backup exists (%s), please remove it manually to continue." % db_old)
        raise Exception("FAILURE")

    # move the current one to the old one
    os.rename(db_cur, db_old)

    # if case when there is no default database we must generate it
    if not os.path.exists(db_def):
        CommandDatabase().run(["--db=sqlite"])

    # now copy default to normal one
    shutil.copy(db_def, db_cur)

    # and remove the old
    os.remove(db_old)

#
#
#
def perform_action(db_str):

    # see what needs to be done
    if db_str == "sqlite":
        return switch_to_sqlite()
    elif db_str == "mysql":
        return switch_to_mysql()
    else:
        pass

    raise Exception("Unknown database specified - %s (must be either sqlite or mysql)" % db_str)
        


#
# main
#
def main():
    verbose = False
    start   = time.time()
    
    # parse command line args
    parser = argparse.ArgumentParser(description='Monitoring database manipulation script.')
    parser.add_argument("--verbose", help="print additional debug information", action="store_true")
    parser.add_argument("--db", help="switch monitoring database to - one of (sqlite|mysql)", required = True)
    
    args  = parser.parse_args()       
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
        
    logging.basicConfig(format='%(asctime)s %(message)s', level=level)
            
    logging.info("Database manipulation script is starting...")
    logging.debug("Script is started at %s" % datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))
    
    perform_action(args.db)
    
    logging.info("Database manipulaton script is finished SUCCESSFULLY in %d seconds!" % (time.time() - start))
    logging.info("Please do not forget to do the following:")
    logging.info("\t1. Restart Apache (httpd) service")
    logging.info("\t2. Click Save and Restart from Web UI")
    


if __name__ == "__main__":
    main()
