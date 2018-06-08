import os
import json
import logging
import datetime
#
#
#
from django.db.models import Sum, Count
from django.utils import timezone

#
#
#
from monitor.models import Event

'''

#
#
#
class LastReporter:

    def __init__(self, folder):
        self.folder = folder

    def run(self):

        # get the previous day
        last_day = timezone.now().date() - datetime.timedelta(days=1)

        # these are all events that occurred on that day
        events = Event.objects.filter(date=last_day)

        # execute one aggregation request
        data = events.aggregate(
            hits  = Count('id'),
            hosts = Count('host', distinct=True),
            ips   = Count('user_ip', distinct=True), 
            users = Count('user_name', distinct=True)
        )

        # and dump it
        logging.info("Number of hits  is %d" % data['hits'])
        logging.info("Number of hosts is %d" % data['hosts'])
        logging.info("Number of ips   is %d" % data['ips'])
        logging.info("Number of users is %d" % data['users'])
        
        name = os.path.join(self.folder, "db", "report.json")
        with open(name, 'w') as fout:
            json.dump(data, fout)
'''