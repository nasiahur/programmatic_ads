import os
import re
import json
import datetime

#
#
#
from _domain.core import Paths, System

#
#
#
from command import Command


#
#
#
class CommandLicense(Command):

    def run(self, path):    

    	name = "license"
        if System.name() == System.WS_WINDOWS:
            name += ".exe"

        exe = os.path.join(Paths.bin_dir(), name)
        
        # run this command
        (exit_code, stdout, stderr) = Command.run(self, [exe, "--path", path])

        if exit_code == 0:

            # for some reason lic command gives out the array of license keys
            array = json.loads(stdout)
            if not len(array) > 0:
                raise Exception("Cannot check license key status, exit code %d, stdout - %s, stderr - %s" % (exit_code, stdout, stderr))

            return array[0]

        else:
            raise Exception("License key check failed; exit code %d, stdout - '%s', stderr - '%s'" % (exit_code, stdout, stderr))


#
# 
#
class LicenseManager:

    def get(self): # return (bool, license|error)
        
        try:
            
            # get contents of license key
            license = CommandLicense().run(Paths.etc_dir())

            # let's try to parse expires field into python date
            license['expires_in'] = self._parse_expires(license['expires'])

            # and return nicely
            return (True, license)

            # color = 'default','cyan'
                    
        except Exception as e:

            return (False, str(e))

    def _parse_expires(self, date_str):

        result = ""

        try:

            # should be something like 'Jan 30 18:52:43 2018 GMT'
            parsed = datetime.datetime.strptime(date_str, "%b %d %H:%M:%S %Y %Z")

            # calculate difference in days between now and expiration date (as parsed is in future - we subtract from it)
            delta = parsed - datetime.datetime.now()

            # and assign the result
            result = str(delta.days)

        except Exception as e:
            print (e)
            pass
        return result

#
#
#
class LicensedDevicesCounter:

    def get(self):

        users = 0
        ips   = 0

        try:
            report_json = os.path.join(Paths.var_dir(), "db", "report.json")

            with open(report_json) as fin:

                data  = json.load(fin)
                users = data['users']
                ips   = data['ips']

        except Exception as e:
            pass

        return max(users, ips)