import traceback

#
#
#
from _domain.core import System, Distrib

#
#
#
from conf_file import ConfReader
    
#
#
#
class SquidConf:

    def get_path(self):

        # windows (for debug only)
        if System.WS_WINDOWS == System.name():
            return r"m:\websafety_extra\src.test\res\squid.conf"

        # freebsd
        if System.WS_FREEBSD == System.name():
            return "/usr/local/etc/squid/squid.conf"

        # debug check
        assert(System.WS_LINUX == System.name())

        # centos and redhat
        if Distrib.WS_CENTOS7 == Distrib.name():
            return "/etc/squid/squid.conf"

        # by default - debian and ubuntu
        return "/etc/squid/squid.conf"

    def get_str(self):

        result = ""

        try:
            
            path   = self.get_path()
            skip   = False
            lines  = ConfReader(path).read_lines(skip)
            result = '\n'.join(lines)

        except Exception as e:

            result  = str(e)
            result += "\n%s\n" % traceback.format_exc()

        return result
    