import os

#
#
#
from _domain.core import Paths, System

#
# python based cache mgr
#
class BinaryCacheMgr:

    @staticmethod
    def full_path():
    	return os.path.join(Paths.bin_dir(), "cachemgr.py")


# print BinaryCacheMgr.full_path()