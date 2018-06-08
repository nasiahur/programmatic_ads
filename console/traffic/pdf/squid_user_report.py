import json
import argparse
import logging
import os

from base_report import *

class SquidUserReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'users', 'users.json')) as users_file:
            users = json.load(users_file)

        users.sort(key=lambda u: u["size"], reverse=True)

        data = []
        categories = []
        for user in users[:10]:
            categories.append(user["value"])
            data.append(user[self.ordering])

        self.build_chart(data, categories, report)
        self.build_detailed_info(users, report)

    def build_detailed_info(self, users, report):
        for user in users[:self.meta['job']['params']['limit_n_entries']]:
            report.add_header("User: %s, Requests: %d, Bandwidth: %s" % (user["value"], user["hits"], formatted_size(user["size"])), H2)
            user_table = [["Visited domains", "Requests", "Bandwidth", "Duration (sec)"]]
            with open(os.path.join(self.report_directory, 'data', 'users', str(user["id"]), 'detailed')) as domains_file:
                lines = domains_file.read().splitlines()
                domains = []
                for line in lines:
                    domain = json.loads(line)
                    domains.append(domain)
                domains.sort(key=lambda d: d["domain"]["size"], reverse=True)
                for domain in domains[:self.meta['job']['params']['limit_n_drilldown']]:
                    user_table.append([domain["domain"]["value"], domain["domain"]["hits"], formatted_size(domain["domain"]["size"]), formatted_duration(domain["domain"]["duration"])])
            report.add_table(user_table, [50, 10, 20, 20])

    def build_chart(self, data, categories, report):
        pass

class SquidUserByBandwidth(SquidUserReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per User (in megabytes)", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)


