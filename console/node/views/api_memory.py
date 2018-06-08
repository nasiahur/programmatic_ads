#
#
#
from _domain.core import Paths, System
from _domain.utils import Command

#
#
#
class CommandFree(Command):

    def run(self):
        result = {
            'mem'  : {'total': 0, 'used': 0, 'free': 0, 'percent': 0},
            'swap' : {'total': 0, 'used': 0, 'free': 0, 'percent': 0}
        }
        if System.WS_FREEBSD == System.name():
            self.run_freebsd(result)        
        
        elif System.WS_LINUX == System.name():
            self.run_linux(result)
        else:            
            assert(System.WS_WINDOWS == System.name())

        return result
            
    def get_freebsd_page_size(self):

        pagesize = 0
        (exit_code, stdout, stderr) = Command.run(self, ["sysctl", "-n", "hw.pagesize"]) 
        if exit_code == 0:
            pagesize = int(stdout)
        
        return pagesize
        
    def get_freebsd_total_mem(self, pagesize):

        (exit_code, stdout, stderr) = Command.run(self, ["sysctl", "-n", "vm.stats.vm.v_page_count"]) 
        if exit_code == 0:
            return pagesize * int(stdout)

        return 0
        
    def get_freebsd_free_mem(self, pagesize):
        
        (exit_code, stdout, stderr) = Command.run(self, ["sysctl", "-n", "vm.stats.vm.v_free_count"]) 
        if exit_code == 0:
            return pagesize * int(stdout)
        return 0
        
    def parse_freebsd_swap(self, data):
        
        # get the [1:] lines from data
        lines = filter(None, data.split('\n')[1:])
        
        # we need to accumulate each column but for now we process only first line
        for line in lines:
        
            # where each line is a collection of fields
            array = filter(None, line.split(' '))
            if len(array) >= 5:
                return (int(array[1])*1024, int(array[2])*1024, int(array[3])*1024)
        return (0, 0, 0)
    
            
    def run_freebsd(self, result):

        pagesize = self.get_freebsd_page_size()

        # update result
        result['mem']['total']   = self.get_freebsd_total_mem(pagesize)
        result['mem']['free']    = self.get_freebsd_free_mem(pagesize)
        result['mem']['used']    = result['mem']['total'] - result['mem']['free']

        used  = float(result['mem']['used'])
        total = float(result['mem']['total'])
        result['mem']['percent'] = int(100 * (used/total))

        # and for memory and swap [total, used, free] array
        swaptotal = 0
        swapfree  = 0
        swapused  = 0
        
        # run for swap
        (exit_code, stdout, stderr) = Command.run(self, ["swapinfo", "-k", "1K"]) 
        if exit_code == 0:

            (swaptotal, swapused, swapfree) = self.parse_freebsd_swap(stdout)

            result['swap']['total']   = swaptotal
            result['swap']['free']    = swapfree
            result['swap']['used']    = swapused
            
            used  = float(result['swap']['used'])
            total = float(result['swap']['total'])
            result['swap']['percent'] = int(100 * (used/total))

    def find(self, array, line):
        for item in array:
            if item.startswith(line):
                v = item[len(line):]
                v = v.strip()
                if v.endswith("kB"):
                    v = v.strip("kB")
                    v = v.strip()                    
                return v
        return ""

    def to_int(self, value_str):
        value_int = 0
        if len(value_str) > 0:
            value_int = int(value_str) * 1024
        return value_int
    
    def run_linux(self, result):

        with open('/proc/meminfo') as fin:
            lines = fin.read().splitlines()

        # memory calculations
        mem_total = self.to_int(self.find(lines, "MemTotal:"))
        mem_free  = 0
        mem_used  = 0

        if len(self.find(lines, "MemAvailable:")) > 0:
            mem_free = self.to_int(self.find(lines, "MemAvailable:"))
            mem_used  = mem_total - mem_free
        else:
            mem_free  = self.to_int(self.find(lines, "MemFree:"))
            mem_bufs  = self.to_int(self.find(lines, "Buffers:"))
            mem_cache = self.to_int(self.find(lines, "Cached:"))
            mem_used  = mem_free + mem_bufs + mem_cache
            if mem_total >= mem_used:
                mem_free = mem_total - mem_used
            else:
                mem_used = mem_total

        result['mem']['total']   = mem_total
        result['mem']['used']    = mem_used
        result['mem']['free']    = mem_free
        result['mem']['percent'] = int(100 * (float(mem_used)/float(mem_total)))

        # swap calculations
        swap_total = self.to_int(self.find(lines, "SwapTotal:"))
        swap_free  = self.to_int(self.find(lines, "SwapFree:"))
        swap_cache = self.to_int(self.find(lines, "SwapCached:"))

        result['swap']['total'] = swap_total
        if swap_total > 0:
            result['swap']['used']    = swap_total - swap_free
            result['swap']['free']    = swap_free
            result['swap']['percent'] = int(100 * (float(swap_total - swap_free)/float(swap_total)))

        return result
        
#
#
#
class Memory:    
    def get(self):
        return CommandFree().run()['mem']
        
#
#
#
class Swap:    
    def get(self):
        return CommandFree().run()['swap']

#
#
#
class CommandDisk(Command):

    def run(self):
        (exit_code, stdout, stderr) = Command.run(self, ["df", "-k", Paths.var_dir()]) 
        if exit_code == 0:
            line = filter(None, stdout.split('\n')[1:2])
            rows = line.split(' ')
            for row in rows:
                if row.find('%') != -1:
                    return row
        return '0%'




#
#
#
class Disk:    
    def get(self):
        return CommandDisk().run()