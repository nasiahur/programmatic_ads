import traceback

#
#
#
from _domain.core import System
from _domain.utils import Command

#
#
#
class NetDeviceDumper:

    def dump_devices(self):

        try:
            # construct args
            args = []
            if System.WS_LINUX == System.name():
                args = ["ip", "addr"]
            elif System.WS_FREEBSD == System.name():
                args = ["ifconfig"]
            else:
                raise Exception("NetDeviceDumper::dump_devices - not implemented on system '%s'" % System.name())

            # and run them
            (ret, stdout, stderr) = Command().run(args)
            if ret != 0:
                raise Exception("Invalid exit code: %d; (%s, %s)" % (ret, stdout, stderr))

            # if we got here then it is fine
            return stdout

        except Exception as e:
            return "ERROR: %s\n%s" % (str(e), traceback.format_exc())

    def dump_device(self, name):

        try:
            # construct args
            args = []
            if System.WS_LINUX == System.name():
                args = ["ip", "addr", "show", name]
            elif System.WS_FREEBSD == System.name():
                args = ["ifconfig", name]
            else:
                raise Exception("NetDeviceDumper::dump_device - not implemented on system '%s'" % System.name())

            # and run them
            (ret, stdout, stderr) = Command().run(args)
            if ret != 0:
                raise Exception("Invalid exit code: %d; (%s, %s)" % (ret, stdout, stderr))

            # if we got here then it is fine
            return stdout

        except Exception as e:
            return "ERROR: %s\n%s" % (str(e), traceback.format_exc())


