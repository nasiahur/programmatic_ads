import traceback

#
#
#
from _domain.utils import Command
from binary_squid import BinarySquid
    

#
#
#
class SquidParse:

    def __init__(self):

        self.exe  = BinarySquid.full_path()
        self.args = [self.exe, "-k", "parse"]

    def get_str(self):

        result = ""

        try:
            (exit_code, stdout, stderr) = Command().run(self.args) 
            if exit_code == 0:
                result = stdout + stderr
            else:
                raise Exception(
                    "Command %s failed.\n\tExit Code: %d\n\tSTDOUT: %s\n\tSTDERR: %s" % (" ".join(self.args), exit_code, stdout, stderr)
                )
        
        except Exception as e:

            result  = str(e)
            result += "\n%s\n" % traceback.format_exc()

        return result