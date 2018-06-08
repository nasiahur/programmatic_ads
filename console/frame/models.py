import os
import re
import shutil


#
# django
#
from django.db import models, connection, transaction
from django.core.management import call_command


#
# business logic
#
from _domain.core  import Paths
from _domain.utils import FileWriter, JsonDumper

#
# ours
#
from utility.zipdir      import zipdir
from squid.generator     import Generator as SquidGenerator
from squid.upgrader      import Upgrader  as SquidUpgrader
from safety.generator    import Generator as SafetyGenerator
from safety.upgrader     import Upgrader  as SafetyUpgrader
from traffic.generator   import Generator as TrafficGenerator
from traffic.upgrader    import Upgrader  as TrafficUpgrader
from node.generator      import Generator as NodeGenerator
from node.upgrader       import Upgrader  as NodeUpgrader
from antivirus.generator import Generator as AntivirusGenerator
from antivirus.upgrader  import Upgrader  as AntivirusUpgrader

#
#
#    
class Profile(models.Model):   

    # config information (needed for sync)
    version   = models.IntegerField(default=0)
    timestamp = models.IntegerField(default=0)

    def generate(self):

        etc_dir = Paths.etc_dir()

        # run all generators first
        NodeGenerator(os.path.join(etc_dir, "node")).generate()
        TrafficGenerator(os.path.join(etc_dir, "traffic")).generate()
        SafetyGenerator(os.path.join(etc_dir, "safety")).generate()
        SquidGenerator(os.path.join(etc_dir, "squid")).generate()
        AntivirusGenerator(os.path.join(etc_dir, "antivirus")).generate()

        # dump the copy of the database to /opt/websafety/var/db
        self.dump_db()

        # update config timestamp
        d = {
            'version'   : self.version,
            'timestamp' : self.timestamp
        }
        FileWriter(etc_dir).write('config.json', JsonDumper().dumps(d))

        # and archive it
        self.archive()

    def dump_db(self):

        output_cur = os.path.join(Paths.var_dir(), "db", "config.dump.json")
        output_new = output_cur + ".new"
        if os.path.isfile(output_new):
            os.unlink(output_new)

        try:
            call_command('dumpdata', '--output=%s' % output_new)

            if os.path.isfile(output_cur):
                os.unlink(output_cur)

            shutil.move(output_new, output_cur)

        except Exception as e:
            print(str(e))

    def archive(self):

        # store zipped version of /opt/websafety/etc to the shared folder       
        zip_dir = os.path.join(Paths.var_dir(), "cluster")
        if not os.path.exists(zip_dir):
            os.makedirs(zip_dir)

        # copy the database
        backup_db_file = os.path.join(Paths.etc_dir(), "config.sqlite")
        db_file        = os.path.join(Paths.var_dir(), "db", "config.sqlite")
        
        try: 
            c = connection.cursor()
            c.execute("BEGIN IMMEDIATE")
            shutil.copyfile(db_file, backup_db_file)
        finally:
            c.close()
            connection.rollback()

        # remove all old configs, only last 10 will stay
        files = [f for f in os.listdir(zip_dir) if os.path.isfile(os.path.join(zip_dir, f))]
        for f in files[:-9]:
            os.remove(os.path.join(zip_dir, f))

        # source and target paths
        etc_dir  = Paths.etc_dir()
        zip_file = os.path.join(zip_dir, "%s-%s.zip" % (str(self.timestamp), str(self.version)))

        # zip it
        zipdir(etc_dir, zip_file)


#
# upgrading
#
class Upgrader(object):

    def __init__(self, dry_run, version):

        # set default values
        major = "6"
        minor = "1"

        # if version hint is set, verify and update major and minor
        if version:

            # see if the hint indicates supported version
            match = re.match(r"(\d+)\.(\d+)", version, re.M|re.I)
            if not match:
                raise Exception("Unsupported version to import: %s" % version)

            major = match.group(1)
            minor = match.group(2)

            if major == "4":
                if minor not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    raise Exception("Unsupported minor number for major %s, minor %s: %s" % (major, minor, version))
        
            elif major == "5":
                if minor not in ["0","1","2"]:
                    raise Exception("Unsupported minor number for major %s, minor %s: %s" % (major, minor, version))

            elif major == "6":
                if minor not in ["0", "1"]:
                    raise Exception("Unsupported minor number for major %s, minor %s: %s" % (major, minor, version))
            else:
                raise Exception("Major number of version to import is unknown: %s" % version)

        # store params
        self.dry_run = dry_run
        self.major   = int(major)
        self.minor   = int(minor)

    @transaction.atomic
    def upgrade(self, etc_dir):

        # import node (sharing)
        NodeUpgrader(self.major, self.minor).upgrade(etc_dir)

        # import squid
        SquidUpgrader(self.major, self.minor).upgrade(etc_dir)

        # import traffic
        TrafficUpgrader(self.major, self.minor).upgrade(etc_dir)

        # import safety
        SafetyUpgrader(self.major, self.minor).upgrade(etc_dir)

        # import antivirus
        AntivirusUpgrader(self.major, self.minor).upgrade(etc_dir)

        # see if we are just testing
        if self.dry_run:

            # oh yes, rollback
            transaction.set_rollback(True)