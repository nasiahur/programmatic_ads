#
#
#
from _domain.core import Paths, System
from _domain.utils import Command

#
# a wrapper for the ps command
#
class CommandPs(Command):

    def __init__(self, username):
        self.username = username

    def run(self):
        if System.WS_FREEBSD == System.name():
            args = ["ps", "-U" , self.username, "-o", "pid,user,cputime,pcpu,rss,pmem,command"]
        else:
            args = ["ps", "-U" , self.username, "-u" , self.username, "-o", "pid,user,cputime,pcpu,rss,pmem,command"]

        # run this command
        (exit_code, stdout, stderr) = Command.run(self, args) 

        # and convert
        if exit_code == 0:
            return self.parse_output(stdout)
        else:
            return {}

    def parse_output(self, data):

        # get the [1:] lines from data
        lines = filter(None, data.split('\n')[1:])

        # create array
        result = []

        for line in lines:
        
            # where each line is a collection of fields
            array = filter(None, line.split(' '))

            # create entry from the first 7 fields
            entry = {
                'pid'       : array[0],
                'user'      : array[1],
                'cpu_time'  : array[2],
                'cpu_usage' : array[3],
                'mem_size'  : array[4],
                'mem_usage' : array[5],
                'path'      : " ".join(array[6:])
            }
            if entry['path'].startswith('ps '):
                continue
            result.append(entry)

        return result

