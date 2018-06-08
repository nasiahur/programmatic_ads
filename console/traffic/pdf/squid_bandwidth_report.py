import json
import argparse
import logging
import os
import datetime

from base_report import *

class SquidBandwidthReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'bandwidth', 'bandwidth.json')) as bandwidth_file:
            bandwidth = json.load(bandwidth_file)

        days = {}
        currentDay = {}
        for day in bandwidth:
            if day["day"] in days.keys():
                days[day["day"]]["duration"] += day["duration"]
                days[day["day"]]["size"] += day["size"]
                days[day["day"]]["domains"] += day["domains"]
                days[day["day"]]["users"] += day["users"]
                days[day["day"]]["hours"].append(day)
            else:
                days[day["day"]] = { "day" : datetime.datetime.fromtimestamp(day["day"] * 24 * 60 * 60).strftime("%Y-%m-%d"), "duration" : day["duration"], "size" : day["size"], "domains" : day["domains"], "users" : day["users"], "hours" : [day] }

        data = []
        categories = []
        for day in days.values():
            categories.append(day["day"])
            data.append(day[self.ordering])

        self.build_chart(data, categories, report)
        self.build_detailed_info(days, report)

    def build_detailed_info(self, days, report):
        for day in days.values():
            report.add_header("Day: %s, Domains: %d, Bandwidth: %d MB, Users: %d" % (day["day"], day["domains"], day["size"] / (1024 * 1024), day["users"]), H2)
            day_table = [["Hour", "Domains", "Bandwidth (MB)"]]
            for hour in day["hours"]:
                day_table.append([hour["hour"], hour["domains"], hour["size"] / (1024 * 1024)])
            report.add_table(day_table, [70, 10, 20])

    def build_chart(self, data, categories, report):
        pass

class SquidBandwidthByDate(SquidBandwidthReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per Day", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)
