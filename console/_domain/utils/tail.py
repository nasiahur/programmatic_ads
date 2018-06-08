#
#
#
from .command import CommandElevated


#
#
#
class CommandTail:

    def run(self, log_file, line_count=256):

        try:

            # construct the args
            tail = "tail"
            args = [tail, "-n", str(line_count), log_file]
                
            # run this command
            (exit_code, stdout, stderr) = CommandElevated().run(args) 

            # and return
            return (exit_code, stdout, stderr)

        except Exception as e:
            return (-1, "", str(e))
