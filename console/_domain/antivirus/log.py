import os

#
#
#
from _domain.core  import System, Paths
from _domain.utils import CommandTail
#
#
#
class WsGsbLogDir:

    @staticmethod
    def get():
        return os.path.join(Paths.var_dir(), "log")

#
#
#
class WsGsbLog:

    def __init__(self):

        self.dir = WsGsbLogDir.get()
        self.log = os.path.join(self.dir, "wsgsbd.log")

    def get_path(self):
        
        return self.log

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
