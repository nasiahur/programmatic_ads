#
# system
#
import re
import sys
import platform

#
# business logic
#
from _domain.core import System
from _domain.utils import Command, FolderInfo

#
# 
#
class CommandDiskFree(Command):

    def run(self, folder):

        # assume failure
        success   = False
        exit_code = -1
        stdout    = ""
        stderr    = ""

        try:    
            # run this command
            (exit_code, stdout, stderr) = Command.run(self, ["df", "-h", "-l", folder]) 

            # and mark success
            success = True
        except Exception as e:
            stderr  = str(e)

        # the data
        data = {
            'error': stderr,
            'size' : '',
            'used' : '',
            'avail': '',
            'ratio': ''
        }

        # check if we were successful
        try:
            if success:

                # get the most valud
                array = self.parse(stdout)
                
                data['size']  = array[1]
                data['used']  = array[2]
                data['avail'] = array[3]
                data['ratio'] = array[4]

        except Exception as e:
            success       = False
            data['error'] = str(e)
        
        return (success, data)

    def parse(self, data):
        lines = self.untitle(data)
        lines = self.unwrap(lines)

        return filter(None, lines[0].split(' '))

    def untitle(self, data):

        lines = []
        for line in data.split('\n'):

            match = re.match(r'^filesystem.*', line.lower())
            if not match:    
                line = line.strip()                            
                if len(line) > 0:
                    lines.append(line)

        return lines

    def unwrap(self, lines):

        result   = []
        combined = ""

        for line in lines:

            if len(combined) > 0:
                result.append(combined + " " + line)
                combined = ""
            else:
                if self.short(line):
                    combined = line
                else:
                    result.append(line)
        return result

    def short(self, line):
        if len(line.split(' ')) > 4:
            return False
        return True

#
#
#
class CommandCpuUsage(Command):

    def run(self):

        try:
            args = ["top", "-d", "0.5", "-b", "-n2"]
            if System.WS_FREEBSD == System.name():
                args = ["top", "-d", "2", "-b"]
                
            # run top command twice (it gives correct output only second time)
            (exit_code, stdout, stderr) = Command.run(self, args) 
            if exit_code != 0:
                raise Exception("Cannot run top command, exit code: %d, stdout: %s, stderr: %s" % (exit_code, stdout, stderr))
                
            # parse it
            return self.parse(stdout)

        except Exception as e:
            return 0

    def parse(self, data):
        (us, sy) = self.parse_cpu(data)
        
        vus = self.parse_value(us)
        vsy = self.parse_value(sy)

        return vus + vsy

    def parse_value(self, str):
    
        reg_str = r'\s*(\d*.\d*)\s*\%?[usy]+\s*$'    
        if System.WS_FREEBSD == System.name():
            reg_str = r'\s*(\d*.\d*)\s*\%?\s.*$'    

        match = re.match(reg_str, str)
        if match:
            return float(match.groups()[0])
        return float(0)
    
    def parse_cpu(self, data):
    
        # parse out the lines
        lines = []
        for line in data.split('\n'):
        
            reg_str = r'\%?cpu\(s\)\:(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)'
            if System.WS_FREEBSD == System.name():
                reg_str = r'cpu\:(.*),(.*),(.*),(.*),(.*)'

            match = re.match(reg_str, line.lower())
            if match:
                us = match.groups()[0]
                sy = match.groups()[1]
                if System.WS_FREEBSD == System.name():
                    sy = match.groups()[2]
                lines.append( (us, sy) )
                
        if len(lines) >= 2:
            return lines[1]
        if len(lines) == 1:
            return lines[0]
            
        return ("0","0")



#
# 
#
class CommandUptime(Command):

    def run(self):
        try:    
            # run this command
            (exit_code, stdout, stderr) = Command.run(self, ["uptime"]) 

            # and convert
            return stdout
        except Exception as e:
            return str(e)

            
#
#
#
class Uptime:

    def get(self):
        v = CommandUptime().run()
        v = v.replace("\r", "")
        v = v.replace("\n", " ")
        return v

#
# 
#
class CommandIpAddrList(Command):

    def run(self):
        if System.WS_FREEBSD != System.name():
            return self.run_linux()
        else:
            return self.run_freebsd()

    def run_freebsd(self):

        try:
            # run this command
            (exit_code, stdout, stderr) = Command.run(self, ["ifconfig"]) 
            
            # empty result by default
            res = []

            # split the stdout into lines
            lines = stdout.split('\n')
            for line in lines:
                line = line.strip()

                interesting = False
                if line.startswith("inet ") or line.startswith("inet6 "):
                    interesting = True
                if not interesting:
                    continue

                pos = line.find(' ')
                if pos != -1:
                    line = line[pos + 1:]
                    pos  = line.find(' ')
                    if pos != -1:
                        line = line[:pos]

                if line.startswith("127.0.0.1") or line.startswith("::1"):
                    continue

                if line.find("%lo") != -1:
                    continue
                res.append(line)
        
            return res


        except Exception as e:
            return [str(e)]


    def run_linux(self):

        try:    
            # run this command
            (exit_code, stdout, stderr) = Command.run(self, ["ip", "addr"]) 

            # empty result by default
            res = []

            # split the stdout into lines
            lines = stdout.split('\n')
            for line in lines:
                line = line.strip()
                if not line.startswith("inet"):
                    continue

                pos = line.find(' ')
                if pos != -1:
                    line = line[pos + 1:]
                    pos = line.find(' ')
                    if pos != -1:
                        line = line[:pos]

                if line.startswith("127.0.0.1/") or line.startswith("::1/"):
                    continue

                res.append(line)
            
            return res

        except Exception as e:
            return [str(e)]
        
#
#
#   
class SystemInfo:

    def get_hostname(self):
        return platform.node()
        
    def get_arch(self):
        (bits, fmt) = platform.architecture()
        if len(fmt) > 0:
            return "%s, %s" % (bits, fmt)
        else:
            return bits

    def get_nics(self):
        return CommandIpAddrList().run()
        
    def get_pythonver(self):
        v = sys.version
        v = v.replace("\r", "")
        v = v.replace("\n", " ")
        a = v.split()
        return "%s" % (a[0], )
    
    def get_size(self, folder):
        return FolderInfo(folder).get_size()
        
    def get_info(self):
        return "%s, version %s" % (platform.system(), platform.uname()[2])

    def is_pfsense(self):   
        if System.WS_FREEBSD != System.name():
            return False

        try:
            version = open("/etc/version").readlines()[0]
            match   = re.match(r'\d\.\d.*', version)
            if match:
                return True
        except:
            pass        
        return False
