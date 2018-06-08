import json
import argparse
import logging
import os

from base_report import *

class BandwidthReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'days.json')) as days_file:
            days = json.load(days_file)

        data = []
        categories = []
        for day in days:
            categories.append(day["date"])
            data.append(day[self.ordering])
        
        self.build_chart(data, categories, report)
        self.build_detailed_info(days, report)

    def build_detailed_info(self, days, report):
        for day in days:
            report.add_header("Day: %s, Requests: %d, Bandwidth: %d MB, Users: %d" % (day["date"], day["hits"], day["size"] / (1024 * 1024), day["users"]), H2)
            day_table = [["Hour", "Requests", "Bandwidth (MB)"]]
            with open(os.path.join(self.report_directory, 'data', day["date"], 'hours.json')) as hours_file:
                hours = json.load(hours_file)
                for hour in hours:
                    day_table.append([hour["hour"], hour["hits"], hour["size"] / (1024 * 1024)])
            report.add_table(day_table, [70, 10, 20])

    def build_chart(self, data, categories, report):
        pass

class TopBandwidthByDate(BandwidthReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth  per Day", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopBandwidthByHour(BandwidthReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth  per Day", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)
