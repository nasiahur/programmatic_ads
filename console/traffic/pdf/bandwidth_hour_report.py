import json
import argparse
import logging
import os

from base_report import *

class TopBandwidthByHour(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'hours.json')) as hours_file:
            hours = json.load(hours_file)

        data = []
        categories = []
        for hour in hours:
            categories.append(str(hour["hour"]))
            data.append(hour[self.ordering])
        
        self.build_chart(data, categories, report)

    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per Hour", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)