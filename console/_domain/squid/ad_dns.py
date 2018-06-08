import os
import re

#
#
#
from _domain.core import System
from _domain.utils import Command

#
# a wrapper for the dig command - returns server, port tuple
#
class DnsDigger:

    def dig(self, server):
        
        # returns the array of [servers]
        result = []

        try:            
            if System.name() == System.WS_WINDOWS:
                result = self.run_windows(server)
            else:
                result = self.run_linux(server)
        except Exception as e:
            print e
        
        return result

    def run_linux(self, server):

        (exit_code, stdout, stderr) = Command().run(["dig", "srv", server, "+short"]) 

        servers = []

        for line in stdout.split('\n'):

            output = line.split(' ')
            if len(output) != 4:
                continue

            servers.append( (output[3].strip().strip('.'), output[2]) )
            
            # we only take first two
            if len(servers) >= 2:
                break 

        return servers

    def run_windows(self, server):

        (exit_code, stdout, stderr) = Command().run(["nslookup", "-type=SRV", server]) 

        # first collect only interesting lines from output
        name_re = re.compile(".*svr\s*hostname\s*=\s*(.*)$",re.IGNORECASE)
        port_re = re.compile(".*port\s*=\s*(.*)$",re.IGNORECASE)

        # interesting entries
        entries = []

        for line in stdout.split('\r\n'):

            match = name_re.match(line)
            if match:
                entries.append(match.group(1).strip())

            match = port_re.match(line)
            if match:
                entries.append(match.group(1).strip())

        servers = []

        # now make servers out of entries
        if len(entries) > 1:
            if len(entries) >= 4:
                servers.append( (entries[1], entries[0]) )
                servers.append( (entries[3], entries[2]) )
            else:
                servers.append( (entries[1], entries[0]) )

        return servers
