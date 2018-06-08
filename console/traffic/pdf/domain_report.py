import json
import argparse
import logging
import os

from base_report import *

class DomainReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'domains.json')) as domains_file:
            domains = json.load(domains_file)

        data = []
        categories = []
        for domain in domains[:10]:
            categories.append(domain["value"])
            data.append(domain[self.ordering])

        self.build_chart(data, categories, report)
        self.build_detailed_info(domains, report)

    def build_detailed_info(self, domains, report):
        for domain in domains:
            report.add_header("Domain: %s, Requests: %d, Bandwidth: %d MB, Users: %d" % (domain["value"], domain["hits"], domain["size"] / (1024 * 1024), domain["users"]), H2)
            domain_table = [["Users", "Requests", "Bandwidth (MB)"]]
            with open(os.path.join(self.report_directory, 'data', str(domain["id"]), 'users.json')) as users_file:
                users = json.load(users_file)
                for user in users:
                    domain_table.append([user["value"], user["hits"], user["size"] / (1024 * 1024)])
            report.add_table(domain_table, [70, 10, 20])

    def build_chart(self, data, categories, report):
        pass


class TopDomainByRequests(DomainReport):
    def build_chart(self, data, categories, report):
        report.add_header("Requests per Domain (in thousands)", H2)
        dataLabel = lambda x: str(x / 1000) + "K"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopDomainByBandwidth(DomainReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per Domain (in megabytes)", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopDomainByUsers(DomainReport):
    def build_chart(self, data, categories, report):
        report.add_header("Users per Domain", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopDomainByIps(DomainReport):
    def build_chart(self, data, categories, report):
        report.add_header("IPs per Domain", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopBlockedDomainsByRequests(DomainReport):
    def build_chart(self, data, categories, report):
        report.add_header("Requests per Domain", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)







