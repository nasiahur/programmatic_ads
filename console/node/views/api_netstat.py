#
#
#
from _domain.core import Paths, System
from _domain.utils import Command


#
# a wrapper for the netstat command
#
class CommandNetstat(Command):

    def run(self, icap_port="1344"):

        if System.WS_FREEBSD == System.name():
            args = ["netstat", "-an", "-p", "tcp"]
        else:
            args = ["netstat", "--tcp" , "--all", "--numeric" , "--program", "--verbose"]
            
        # run this command
        (exit_code, stdout, stderr) = Command.run(self, args) 

        # and convert
        if exit_code == 0:
            if System.WS_FREEBSD == System.name():
                return self.parse_freebsd_output(stdout, icap_port)
            else:
                return self.parse_linux_output(stdout, icap_port)
        else:
            return []
            
    def parse_freebsd_output(self, data, icap_port):

        # get the [2:] lines from stdout
        lines = filter(None, data.split('\n')[2:])

        # create array of lines
        result = []
        for line in lines:
        
            try:
                # where each line is a collection of fields
                array = filter(None, line.split(' '))
                entry = {
                    'proto'       : array[0],
                    'recvq'       : array[1],
                    'sendq'       : array[2],
                    'local_addr'  : array[3],
                    'remote_addr' : array[4],
                    'state'       : array[5],
                    'path'        : " " # we have no path on FreeBSD
                }
                if entry['local_addr'].endswith("." + icap_port) or entry['local_addr'].endswith(".icap"):
                    result.append(entry)
                elif entry['remote_addr'].endswith("." + icap_port) or entry['remote_addr'].endswith(".icap"):
                    result.append(entry)
            except Exception as e:
                pass

        return result

    def parse_linux_output(self, data, icap_port):

        # get the [2:] lines from stdout
        lines = filter(None, data.split('\n')[2:])

        # create array of lines
        result = []
        for line in lines:

            # where each line is a collection of fields
            array = filter(None, line.split(' '))
            entry = {
                'proto'       : array[0],
                'recvq'       : array[1],
                'sendq'       : array[2],
                'local_addr'  : array[3],
                'remote_addr' : array[4],
                'state'       : array[5],
                'path'        : " ".join(array[6:]) # path may not always be available becase user the Web UI runs at does not have enough rights
            }

            if entry['local_addr'].endswith(":" + icap_port) or entry['local_addr'].endswith(":icap"):
                result.append(entry)
            elif entry['remote_addr'].endswith(":" + icap_port) or entry['remote_addr'].endswith(":icap"):
                result.append(entry)
            else:
                pass

        return result