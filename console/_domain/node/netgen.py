import os
import tempfile

#
#
#
from _domain.core import Paths, System, Distrib
from _domain.utils import CommandElevated

#
#
#
class DebianNetworkSettingsGenerator:

    def generate(self, contents):

        # debug check
        assert(len(contents) > 0)

        # first generate a temporary file in /opt/websafety/etc/node folder (it will be removed after close automatically)
        prefix = "etc_network_interfaces."
        folder = os.path.join(Paths.etc_dir(), "node")

        # write to temp file        
        with tempfile.NamedTemporaryFile(prefix=prefix, dir=folder, delete=True) as temp:

            temp.write(contents)
            temp.flush()

            # call the sudoing binary
            exe  = os.path.join(Paths.bin_dir(), "network_debian.py")
            arg1 = "--file=%s" % temp.name
            arg2 = "--system=%s" % System.name()
            arg3 = "--distrib=%s" % Distrib.name()
            args = [exe, arg1, arg2, arg3]

            # and run it
            (exit_code, stdout, stderr) = CommandElevated().run(args)
            if exit_code != 0:
                raise Exception("Cannot generate network settings. Error: %d, STDOUT: %s, STDERR: %s" % (exit_code, stdout, stderr))
