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
from django.utils.timezone import utc
from django.utils.timezone import make_aware
#
#
#
# TODO: take the port from the config file
class ReportManager:

    def get_reports(self):

        response = ""
        
        resp = None
        try:
            url  = 'http://127.0.0.1:18888/reporting/reports'
            resp = urllib2.urlopen(url)
            response = resp.read()
        except urllib2.URLError as e:
            return { 'success' : False, 'error' : e.reason, 'reports' : [] }
        finally:
            if resp is not None:
                resp.close()

        # convert
        reports = json.loads(response)
        result = { 'success' : True, 'error' : '', 'reports' : [] }
        for report in reports:
            if report['failed']:
                status = 'Failed'
            elif int(report['progress']) != 100:
                status = 'In progress'
            else:
                status = 'Completed'
            progress = report['progress']
            name = report['name']
            id = report['id']
            start = datetime.datetime.strptime(report['start'], '%Y-%m-%d')
            end = datetime.datetime.strptime(report['end'], '%Y-%m-%d')
            builtOn = datetime.datetime.strptime(report['builtOn'], '%Y-%m-%dT%H:%M:%SZ')
            builtOn = make_aware(builtOn, utc)
            result['reports'].append( { 'id' : id, 'name' : name, 'start' : start, 'end' : end, 'progress' : progress, 'status' : status, 'builtOn' : builtOn } )
        return result

        
    def create_report(self, job_name):
        response = ""
        
        resp = None
        try:
            url = 'http://127.0.0.1:18888/reporting/reports/new?'
            url = url + 'id=' + job_name
            
            resp = urllib2.urlopen(url)
            response = resp.read()
        except urllib2.URLError as e:
            return { 'success' : False, 'error' : e.reason }
        finally:
            if resp is not None:
                resp.close()

        # convert
        result = { 'success' : True, 'error' : '' }
        return result