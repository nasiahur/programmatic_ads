import os

#
#
#
from _domain.core import System

#
#
#
class BinaryKlist:

    @staticmethod
    def full_path():

        if System.name() == System.WS_FREEBSD:
            return "ktutil"

        return "klist"
