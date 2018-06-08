import json
import argparse
import logging
import os

from base_report import *

class UserReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'users.json')) as users_file:
            users = json.load(users_file)

        data = []
        categories = []
        for user in users[:10]:
            categories.append(user["value"])
            data.append(user[self.ordering])

        self.build_chart(data, categories, report)
        self.build_detailed_info(users, report)

    def build_detailed_info(self, users, report):
        for user in users:
            report.add_header("User: %s, Requests: %d, Bandwidth: %d MB, Domains: %d" % (user["value"], user["hits"], user["size"] / (1024 * 1024), user["domains"]), H2)
            user_table = [["Visited domains", "Requests", "Bandwidth (MB)"]]
            with open(os.path.join(self.report_directory, 'data', str(user["id"]), 'domains.json')) as domains_file:
                domains = json.load(domains_file)
                for domain in domains:
                    user_table.append([domain["value"], domain["hits"], domain["size"] / (1024 * 1024)])
            report.add_table(user_table, [70, 10, 20])

    def build_chart(self, data, categories, report):
        pass


class TopUserByRequests(UserReport):
    def build_chart(self, data, categories, report):
        report.add_header("Requests per User (in thousands)", H2)
        dataLabel = lambda x: str(x / 1000) + "K"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopUserByBandwidth(UserReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per User (in megabytes)", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopUserByDomains(UserReport):
    def build_chart(self, data, categories, report):
        report.add_header("Domains per User (in hundreds)", H2)
        dataLabel = lambda x: str(x / 100) + "H"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopUserByBlockedDomains(UserReport):
    def build_chart(self, data, categories, report):
        report.add_header("Domains per User", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)







