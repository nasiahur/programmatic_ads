import json
import argparse
import logging
import os
import math
from decimal import *

from pdf_report import *

def formatted_size(actual_size):
    if actual_size is None or int(actual_size) == 0:
        return 0
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    measure = 0

    if actual_size > 1024 * 1024 * 1024 * 1024 and actual_size <= 1024 * 1024 * 1024 * 1024 * 1024:
        measure = 4
    elif actual_size > 1024 * 1024 * 1024 and actual_size <= 1024 * 1024 * 1024 * 1024:
        measure = 3
    elif actual_size > 1024 * 1024 and actual_size <= 1024 * 1024 * 1024:
        measure = 2
    elif actual_size > 1024 and actual_size <= 1024 * 1024:
        measure = 1

    f = len(str(math.floor(actual_size / math.pow(1024, measure))));
    if f > 3:
        precision = 0
    else:
        precision = 3 - f
    return ("{:." + str(precision) + "f}").format(actual_size / math.pow(1024, measure)) + units[measure]


def formatted_duration(duration):
    seconds = math.floor(duration / 1000);
    if seconds == 0:
        return str(duration) + " ms"
        
    minutes = math.floor(duration / 60000);
    if minutes == 0:
        return str(seconds) + " s"

    hours = math.floor(minutes / 60);
    if hours == 0:
        return str(minutes) + " min"

    return str(hours) + " h"

# Supported ordering 
#     by hits, size, domains
class BaseReport(object):
    def __init__(self, report_directory, ordering):
        self.report_directory = report_directory
        self.ordering = ordering
        self.meta = None

    def build(self):

        # create document header
        with open(os.path.join(self.report_directory, 'data', 'meta.json')) as meta_file:
            self.meta = json.load(meta_file)

        report = PdfReport("Diladele Web Safety Report : %s" % self.meta["name"], self.meta, os.path.join(self.report_directory, 'data'))
        report.add_report_header()

        self.build_content(report)
        report.build()

    def build_content(self, report):
        pass
