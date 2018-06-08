import os
import json
import socket
import platform
import itertools
import urllib2
import datetime
import time
import calendar

#
# business logic
#
from _domain.utils import Command


#
#
#
from django.conf import settings
from traffic.surfing import SurfingRecord
from traffic.models import *
from django.utils.timezone import utc

#
#
#
class CommandHistory(Command):

    def run(self, column_name, column_value, order_by, limit, asc):
        response = ""
        try:
            # TODO: take the port from the config file
            url = 'http://127.0.0.1:18888/monitoring/analytics/icap/getlastitems?limit=' + str(limit)
            
            if column_name:
                url = url + '&cn=' + column_name
                url= url + '&cv=' + column_value

            if order_by:
                url = url + '&order_by=' + order_by

            if asc:
                url = url + '&asc=ASC'
            else:
                url = url + '&asc=DESC'

            resp = urllib2.urlopen(url)
            response = resp.read()
        except urllib2.URLError as e:
            return []
        finally:
            resp.close()

        # convert
        events = json.loads(response)
        return events

#
#
#
class HistoryManager:
    #
    #
    #
    def get_all(self, column_name, column_value, order_by, number, asc):

        result = { 'success' : False, 'error' : '', 'events' : [] }

        try:
            events = CommandHistory().run(column_name, column_value, order_by, number, asc)
            records = []
            for item in events:
                records.append(self.create_surfing_record(item))
            return records
        except Exception as e:
            return []
        return result

    def create_surfing_record(self, item):
        r = SurfingRecord()
        r.server = item['server']               # string
        r.timestamp = item['timestamp']         # string original timestamp in UTC
        r.hour = item['hour']                   # string hour 0-23 from
        r.iid = item['iid']
        r.duration = item['duration']           # int
        r.timing = item['timing']               # int
        r.size = item['size']                   # int
        r.size_approx = item['size']
        r.trusted = item['trusted']
        r.message = item['message']             # icap::request_type (string)
        r.user_ip = item['user_ip']             # string
        r.user_name = item['user_name']         # string
        r.user_agent = item['user_agent']
        r.user_eui = item['user_eui']
        r.policy = item['policy']               # string
        r.member = item['member']               # string        
        r.content_type = item['content_type']   # string
        r.module = item['module']               # ql::br::module_type (string)
        r.level = item['level']                 # icap::scan_level (string)
        r.verdict = item['verdict']             # icap::scan_verdict (string)
        r.offensive = item['offensive']
        r.unproductive = item['unproductive']
        r.param1 = item['param1']               # string
        r.param2 = item['param2']               # string
        r.mtime = item['mtime']                 # int
        r.host = item['host']                   # string
        r.tld = item['tld']
        r.method = item['method']
        r.scheme = item['scheme']
        r.path = item['path']                   # string
        r.query = item['query']
        r.ref_scheme = item['ref_scheme']
        r.ref_host = item['ref_host']
        r.ref_path = item['ref_path']

        r.url = r.scheme + '://' + r.host + r.path + r.query  #item['url']
    
        
        r.flags = r.parse_flags(item['scanflags'])                  # array
        r.categories = r.parse_categories(item['categoryflags'])    # array

        r.timestamp = datetime.datetime.strptime(r.timestamp, "%Y-%m-%dT%H:%M:%SZ")
        #st = time.strptime(r.timestamp, "%Y-%m-%dT%H:%M:%SZ")
        #r.timestamp = datetime.datetime.utcfromtimestamp(calendar.timegm(st))
        #r.timestamp = r.timestamp.replace(tzinfo=utc)
        #r.timestamp
        return r
