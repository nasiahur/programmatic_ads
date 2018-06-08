import os
import re
import pytz

#
#
#
from _domain.core import Paths, System, Distrib
from _domain.utils import Command, CommandElevated


#
# time zone
#
class TimeZone:

    def __init__(self):
        
        self.default = "Europe/Amsterdam"        
        
    def configured_tz(self):

        # assume default        
        value = self.default

        # set the value 
        system_str = System.name()         
        if system_str == System.WS_WINDOWS:
            pass
        if system_str == System.WS_LINUX:
            value = self.configured_tz_linux()
        if system_str == System.WS_FREEBSD:
            pass

        # debug check
        assert(len(value) > 0)

        # and return
        return value

    def configured_tz_linux(self):

        # debug check
        assert(System.name() == System.WS_LINUX)

        # assume default
        value = self.default

        # see if this is centos style
        if Distrib.WS_CENTOS7 == Distrib.name():

            etc_localtime = "/etc/localtime"
            usr_zoneinfo  = "/usr/share/zoneinfo/"

            # see if local time is a link or not
            if os.path.islink(etc_localtime):

                value = os.path.realpath(etc_localtime)
                if value.startswith(usr_zoneinfo):
                    value = value[len(usr_zoneinfo):]

        else:

            # ok this is debian style then
            with open('/etc/timezone') as fin:
                value = fin.read()                
                value = value.strip()

        # return nicely
        return value

    def running_tz(self):

        value = self.running_tz_str()
        pos   = value.find('(')
        if pos != -1:
            value = value[:pos]
            value = value.strip()

        return value

    def running_tz_str(self):

        # for debug only
        if System.WS_WINDOWS == System.name():
            return "Europe/London"

        # this is the value to return
        value = ""

        if System.name() == System.WS_LINUX:

            # on linux we call timedatectl
            args  = ["timedatectl", "status", "--no-pager"]
        
            (exit_code, stdout, stderr) = Command().run(args) 
            if exit_code != 0:
                raise Exception("Cannot run command %s, exit code: %d, error message:\n%s" % (" ".join(args), exit_code, stdout + stderr))

            for line in stdout.split('\n'):
                pos = line.find(":")
                if pos == -1:
                    continue

                left  = line[:pos].strip()
                right = line[pos + 1:].strip()

                match = re.match( r'.*time.*zone.*', line, re.M|re.I)
                if match:
                    value = right

        if System.name() == System.WS_FREEBSD:

            # TODO
            # on freebsd it is a little different; the /etc/localtime can be either a symlink or a copy of any file
            # including one in subdirectories of /usr/share/zoneinfo. We need to first find that file and then
            # parse out the zone information as folder/subfolder starting from /usr/share/zoneinfo as root, complex!
            raise Exception("NOT_IMPL of FreeBSD")
            
        return value

    def set(self, value):

        assert(len(value) > 0)

        # check the provided timezone indeed exists in the pytz
        if value not in pytz.all_timezones:
            raise Exception("Wrong timezone %s (not found pytz.all_timezones)" % value)

        # save the new timezone into the system
        exe  = os.path.join(Paths.bin_dir(), "timezone.py")
        arg1 = "--timezone=%s" % value
        arg2 = "--system=%s" % System.name()
        arg3 = "--distrib=%s" % Distrib.name()
        args = [exe, arg1, arg2, arg3]

        (ret, stdout, stderr) = CommandElevated().run(args)

        # the system zone is set if return value is 0
        if ret == 0:

            # also generate the timezone.setting file
            tz_file = os.path.join(Paths.var_dir(), "console", "console", "timezone.setting")
            with open(tz_file,"w") as fout:
                fout.write(value)

        # and return
        return (ret, stdout, stderr)
