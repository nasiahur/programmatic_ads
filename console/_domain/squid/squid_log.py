import os

#
#
#
from _domain.core  import System
from _domain.utils import CommandTail
#
#
#
class SquidLogDir:

    @staticmethod
    def get():

        if System.WS_WINDOWS == System.name():
            return "c:\\Squid\\var\\log\\squid"

        # in ubuntu, debian, centos, freebsd
        value = "/var/log/squid"
        if not os.path.isdir(value):

            # on pfsense
            value = "/var/squid/logs"

        # and return nicely
        return value

#
#
#
class SquidLog:

    def __init__(self):

        self.dir = SquidLogDir.get()
        self.log = os.path.join(self.dir, self.log_name)

    def get_size(self):

        size = 0
        if os.path.exists(self.log):
            size = os.path.getsize(self.log)

        return size

    def get_contents(self, line_count, include, exclude):

        (code, stdout, stderr) = CommandTail().run(self.log, line_count)
        if 0 != code:
            return stderr

        # got output, do exclusions
        if len(exclude) > 0:
            lines = []
            for line in stdout.split('\n'):
                if line.find(exclude) == -1:
                    lines.append(line)

            stdout = '\n'.join(lines)

        # do inclusions
        if len(include) > 0:
            lines = []
            for line in stdout.split('\n'):
                if line.find(include) != -1:
                    lines.append(line)
            stdout = '\n'.join(lines)

        return stdout


#
#
#
class SquidAccessLog(SquidLog):

    log_name = 'access.log'

#
#
#
class SquidCacheLog(SquidLog):

    log_name = 'cache.log'