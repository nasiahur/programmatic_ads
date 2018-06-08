#
#
#
import os

#
#
#
from netaddr_utils import *

#
#
#
class Iface:

    def __init__(self):

        self.logical_name   = ""
        self._addr_family   = ""
        self._config_method = ""
        self.options        = {}

    def set_addr_family(self, value):
        assert(value in ["inet", "inet6"])
        self._addr_family = value

    def get_addr_family(self):
        return self._addr_family

    def get_config_method(self):
        return self._config_method

    def set_config_method(self, value):
        assert(value in ["static", "dhcp", "loopback", "manual"])
        self._config_method = value

    def get_address(self):
        return self.get_option('address')

    def get_netmask(self):
        return self.get_option('netmask')

    def get_gateway(self):
        return self.get_option('gateway')

    def get_dns_search(self):
        return self.get_option('dns-search')

    def get_dns_nameservers(self):
        value = self.get_option('dns-nameservers')
        items = Splitter.split(value,' ')
        return items

    def get_option(self, name):
        return self.options.get(name, '')

#
#
#
class Interfaces(object):

    def __init__(self):

        self.autos    = []
        self.ifaces   = []
        
#
#
#
TOKEN_EOF   = 0
TOKEN_AUTO  = 1
TOKEN_IFACE = 2

#
#
#
class Lexer:

    def __init__(self, lines):
        self.lines = lines

    def get(self):

        while True:
            
            line = self.pop()
            if line is None:
                return (TOKEN_EOF, None)
        
            elif line.startswith("auto"):                            
                return (TOKEN_AUTO, line[len("auto"):].lstrip())
        
            elif line.startswith("iface"):

                value = line[len("iface"):].lstrip()

                while True:

                    nextl = self.pop()
                    if nextl is None:
                        return (TOKEN_IFACE, value)

                    if nextl.startswith("auto") or nextl.startswith("iface"):
                        self.unpop(nextl)
                        return (TOKEN_IFACE, value)

                    value += '\n' + nextl

            else:
                # ignore this line and continue
                continue

    def pop(self):
        if len(self.lines) == 0:
            return None
        return self.lines.pop(0)

    def unpop(self, line):
        self.lines.insert(0, line)

#
#
#
class PreProcessor:

    @staticmethod
    def process(lines):

        contents = []

        while(len(lines) > 0):
            line = lines.pop(0)
            line = line.strip()
            
            if not len(line):
                continue
            if line.startswith('#'):
                continue

            contents.append(line)

        return contents

#
#
#
class Parser:

    def parse(self, file):

        # this is the value to return
        interfaces = Interfaces()

        # read the file
        lines = Reader.read(file)
        lines = PreProcessor.process(lines)

        # get all tokens
        lexer = Lexer(lines)
        while(True):

            (token_type, token_str) = lexer.get()
            
            if token_type == TOKEN_EOF:
                break
            
            if token_type == TOKEN_AUTO:

                # get the physical interface
                physical = self.parse_auto(token_str)

                # and append it
                if physical not in interfaces.autos:
                    interfaces.autos.append(physical)

            if token_type == TOKEN_IFACE:

                # get the logical interface
                logical = self.parse_iface(token_str)

                # and append it
                interfaces.ifaces.append(logical)
                
        # and return the parsed value
        return interfaces

    def parse_auto(self, token_str):

        items = Splitter.split(token_str)
        if not len(items):
            raise Exception("Cannot parse token auto directive: %s" % token_str)

        return items[0]

    def parse_iface(self, token):

        lines = Splitter.split(token, '\n')
        if len(lines) < 1:
            raise Exception("Cannot parse token iface directive (too small number of lines): %s" % token)

        # parse the first line        
        first = lines.pop(0)
        items = Splitter.split(first)
        if not len(items):
            raise Exception("Cannot parse token iface directive: %s" % token)

        # assign variables (remember parser does not support inherits so we only parse 'iface ens160 inet static')
        iface = Iface()

        iface.logical_name  = items[0]
        iface.set_addr_family(items[1])
        iface.set_config_method(items[2])

        # now parse the rest of lines
        while len(lines) > 0:
            self.parse_iface_option(lines.pop(0), iface)

        return iface

    def parse_iface_option(self, line, iface):

        items = Splitter.split(line)
        if len(items) < 1:
            return

        # set name
        name = items.pop(0)
        if name == "post-up":
            name = "up"
        if name == "pre-down":
            name = "down"
        
        # set value
        value = " ".join(items)

        # assign
        iface.options[name] = value

#if __name__ == "__main__":
#
#    f = Parser().parse("netaddr_debian_interfaces")
#    print f.autos
#    print f.ifaces
    