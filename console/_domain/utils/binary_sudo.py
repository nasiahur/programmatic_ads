import os

#
#
#
class BinarySudo:

    @staticmethod
    def full_path():

        # in ubuntu, debian, centos
        exe = "/usr/bin/sudo"
        if not os.path.isfile(exe):

            # on freebsd
            exe = "/usr/local/bin/sudo"

        # and return
        return exe
