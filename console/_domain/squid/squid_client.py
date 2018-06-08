#
#
#
import os
import traceback

#
#
#
from _domain.core import System
from _domain.utils import Command

#
#
#
from binary_squid_client import BinarySquidClient

#
#
#
class SquidClient:

    def __init__(self, host, port):

        self.exe  = BinarySquidClient.full_path()
        self.host = host
        self.port = port

        # adjust host if needed
        if not self.host:
            self.host = "127.0.0.1"

    def mrginfo_str(self):
        return self.get_str("info")

    def dnsinfo_str(self):    
        return self.get_str("idns")

    def counters_str(self): 
        return self.get_str("counters")

    def min5_str(self): 
        return self.get_str("5min")

    def min60_str(self): 
        return self.get_str("60min")

    def utilization_str(self): 
        return self.get_str("utilization")

    def username_cache_str(self): 
        return self.get_str("username_cache")

    def negotiateauthenticator_str(self): 
        return self.get_str("negotiateauthenticator")

    def ntlmauthenticator_str(self): 
        return self.get_str("ntlmauthenticator")

    def basicauthenticator_str(self): 
        return self.get_str("basicauthenticator")

    def client_list_str(self): 
        return self.get_str("client_list")

    def active_requests(self):

        result = {
            'error'   : False,
            'message' : '',
            'items'   : []
        }

        try:
            value = self.get_str_unsafe("active_requests")            
            pos   = value.find("\r\n\r\n")
            if pos != -1:
                value = value[pos+4:]

            from squid_active_requests import SquidActiveRequestsParser

            result['items'] = SquidActiveRequestsParser(value).parse()

        except Exception as e:

            result['error']   = True
            result['message'] = "Exception: %s\n\nCall stack:\n%s" % (str(e), traceback.format_exc())

        return result


    def get_str(self, request): 

        result = ""

        try:
            result = self.get_str_unsafe(request)            

        except Exception as e:

            result  = str(e)
            result += "\n%s\n" % traceback.format_exc()

        return result

    def get_str_unsafe(self, request):

        arg_port = "-p"
            
        # bad fix - need to base decision on squid version and not on the system
        if System.name() == System.WS_FREEBSD:
            arg_port = "-a"

        args = [self.exe, arg_port, str(self.port), "-h", self.host, "mgr:%s" % request]

        (exit_code, stdout, stderr) = Command().run(args) 
        if exit_code == 0:
            pos = stdout.find("\r\n\r\n")
            if pos != -1:
                stdout = stdout[pos+4:]

            return stdout

        # if we got here everything failed
        raise Exception(
            "Command %s failed.\n\tExit Code: %d\n\tSTDOUT: %s\n\tSTDERR: %s" % (" ".join(args), exit_code, stdout, stderr)
        )

