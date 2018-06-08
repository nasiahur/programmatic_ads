import os
import platform

#
# constant predefined paths for the domain folder
#
class Paths:

    @staticmethod
    def install_dir():

        if platform.system() == "Windows":
            return r"m:\websafety\src.res\opt\websafety"

        return "/opt/websafety"

    @staticmethod
    def bin_dir():
        return os.path.join(Paths.install_dir(), "bin")

    @staticmethod
    def etc_dir():
        return os.path.join(Paths.install_dir(), "etc")

    @staticmethod
    def var_dir():
        return os.path.join(Paths.install_dir(), "var")