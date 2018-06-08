#
# active_requests.py
#
import re
import urlparse

#
# returns array of dictionaries
#
class SquidActiveRequestsParser:

    def __init__(self, data_str):
        self.data = data_str.replace("\r", "").split("\n\n")
        
    def parse(self):
        connections = []
        while True:
            connection = self.parse_one()
            if connection is None:
                return connections
            else:
                # sometimes we get empty connections parsed
                if not 'ip' in connection or not 'uri' in connection:
                    continue

                # we are not interested in squid client connections
                if not connection['uri'].startswith("cache_object://"):
                    connections.append(connection)

    def parse_one(self):

        if len(self.data) <= 0:
            return None

        fields = {}
        for field in self.data.pop(0).split("\n"):

            # get the field            
            field = field.strip().strip('\n').strip('\t')            

            # split a field into result, name, value tuple
            (r, n, v) = self.parse_field(field)
            if r != True:
                continue

            # get host from uri
            if n == "uri":
                fields["host"] = field#self.parse_host(v)

            # save the field
            fields[n] = field#v
            print(field)
        return fields

    def parse_host(self, uri):

        obj = urlparse.urlparse(uri)
        if obj.hostname != None:
            return obj.hostname

        # could happen when parsing www.domain.name:443
        pos = uri.find("://")
        if pos != -1:
            uri = uri[pos+3:]

        pos = uri.rfind(":")
        if pos != -1:
            uri = uri[:pos]

        return uri

    def parse_field(self, field):

        # see if this is an exluded field
        excluded = [
            "Connection: ", "FD ", "FD desc:", "in:", "out.", "req_sz ", "delay_pool", "entry", "logType", "local:", "nrequests:", "start "
        ]
        for exclusion in excluded:
            if field.startswith(exclusion):
                return (False, None, None)

        # ok not excluded, parse it
        pos = field.find("Connection: ")
        if pos != -1:
            return (True, "connection", field[pos+12:])

        pos = field.find("username ")
        if pos != -1:
            return (True, "user", field[pos+9:])

        pos = field.find("req_sz ")
        if pos != -1:
            return (True, "req_sz", field[pos+7:])

        pos = field.find("uri ")
        if pos != -1:
            return (True, "uri", field[pos+4:])

        pos = field.find("remote: ")
        if pos != -1:
            tmp  = field[pos+8:]
            pos2 = tmp.rfind(':')
            if pos2 != -1:
                tmp = tmp[:pos2]
            return (True, "ip", tmp)

        match = re.match(r'start .*\((.*)\)$', field, re.M|re.I)
        if match:
            return (True, "age", match.group(1))

        return (True, "name", field)

#
# test it
#
'''
with open("m:\\websafety\\src.res\\opt\\websafety\\var\\console\\squid\\active_requests.txt", "rb") as fin:
    data   = fin.read()
    parser = SquidActiveRequestsParser(data)
    items  = parser.parse()
    for item in items:
        print item['ip']
        print item['host']
        print item['uri']
        print item['user']

        print ""
        print ""

'''