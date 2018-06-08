#
#
#
import os
import sys
import json
import traceback

#
#
#
from _domain.core import System, Paths
from _domain.utils import Command

#
#
#
class PseudoAuthDumper:

    def __init__(self, server1, port1, server2, port2, token):

        self.exe     = os.path.join(Paths.bin_dir(), "inspector_auth.py")
        self.server1 = server1
        self.port1   = str(port1)
        self.server2 = server2
        self.port2   = str(port2)
        self.token   = token

    def dump(self):

        args = [ sys.executable, self.exe, "--server1", self.server1, "--port1", self.port1, "--dump" ]

        if self.server2:
            args.extend( ["--server2", self.server2, "--port2", self.port2] )

        if self.token:
            args.extend( ["--token", self.token] )

        (exit_code, stdout, stderr) = Command().run(args) 
        if exit_code == 0:
            return json.loads(stdout)

        # if we got here everything failed
        raise Exception(
            "Command %s failed.\n\tExit Code: %d\n\tSTDOUT: %s\n\tSTDERR: %s" % (" ".join(args), exit_code, stdout, stderr)
        )