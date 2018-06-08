#
#
#
import socket
import platform

#
#
#
from django import forms


#
# represents both IPv6 and IPv4 addresses; constructed by AddressParser
#
class Address:

    def __init__(self, is_ipv6, nvalue):

        self.is_ipv6 = is_ipv6
        self.nvalue  = nvalue

#
# constructs Addresses from strings (both IPv4 and IPv6)
#
class AddressParser:

    def parse(self, value):

        try:
            return self._as_v4(value)            
        except socket.error as e1:
            try:
                return self._as_v6(value)
            except socket.error as e2:
                pass

            raise Exception("Cannot parse %s as IPv4 or IPv6, error1: %s, error2: %s" % (value, str(e1), str(e2)))

    def _as_v4(self, value):
        return Address(False, socket.inet_aton(value))

    def _as_v6(self, value):
        if platform.system() == "Windows":
            import win_inet_pton
            return Address(True, win_inet_pton.inet_pton(socket.AF_INET6, value))
        else:
            return Address(True, socket.inet_pton(socket.AF_INET6, value))
        

#
# form validator for IP addresses
#
class AddressIP:

    def check(self, value):

        value = value.strip()
        try:
            a = AddressParser().parse(value)            
        except Exception as e: 
            raise forms.ValidationError("Incorrect IP address specified, error: " + str(e))
        return value

#
#
#
class PortIP:
    def check(self, value):
        n = int(value)
        if n < 1 or n > 65535:
            raise forms.ValidationError("Incorrect IP Port specified, must be within [1, 65535]")
        return value
            
#
#
#
class AddressRange:

    def check(self, value):

        # trim the value
        value = value.strip()

        # split in into array of 2
        array = value.split("-")
        if len(array) != 2:
            raise forms.ValidationError("Specified IP address range is incorrect. Address ranges should be specified using IP1-IP2 syntax");

        v1 = array[0].strip()
        v2 = array[1].strip()

        # parse both
        try:
            a1 = AddressParser().parse(v1)
            a2 = AddressParser().parse(v2)

            # check the types
            if a1.is_ipv6 != a2.is_ipv6:
                raise Exception("IPv4 and IPv6 addresses cannot be mixed")

            # check order
            if a1.nvalue >= a2.nvalue:
                raise Exception("IP1 in range should be strictly less than IP2")

        except Exception as e:
            raise forms.ValidationError("Specified IP address range is incorrect; error: %s" % str(e))

        return "%s-%s" % (v1, v2)
           
#
#
#
class AddressSubnet:

    def check(self, value):

        # trim the value
        value = value.strip()

        # split in into array of 2
        array = value.split("/")
        if len(array) != 2:
            raise forms.ValidationError("Specified IP subnet is incorrect. Subnets should be specified using CIDR syntax (IP/NETMASK)");

        v1 = array[0].strip()
        v2 = array[1].strip()

        try:
            a = AddressParser().parse(v1)
            m = int(v2)

            if a.is_ipv6 == False:
                if m >= 32 or m < 1:
                    raise Exception("IPv4 network mask must be within [1:31]")
            else:
                if m >= 128 or m < 1:
                    raise Exception("IPv6 network mask must be within [1:127]")

        except Exception as e:
            raise forms.ValidationError("Specified IP address range is incorrect; error: %s" % str(e))

        return "%s/%s" % (v1, v2)
