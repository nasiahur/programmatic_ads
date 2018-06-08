import os

#
#
#
from _domain.core import Paths, System

#
# new python based cert mgr
#
class BinaryCertMgr:

    @staticmethod
    def full_path():
    	return os.path.join(Paths.bin_dir(), "certmgr.py")


# print BinaryCertMgr.full_path()