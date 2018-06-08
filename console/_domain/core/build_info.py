#
#
#
from sys_info import System

#
#
#
class Build:

    @staticmethod
    def version():

        if System.WS_WINDOWS == System.name():
            return "0.0.0.0"

        return "6.2.0.FD48"