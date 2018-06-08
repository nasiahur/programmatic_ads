import json
import argparse
import logging
import os

from base_report import *

class SquidDomainReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'domains', 'domains.json')) as domains_file:
            domains = json.load(domains_file)

        domains.sort(key=lambda d: d["size"], reverse=True)
        data = []
        categories = []
        for domain in domains[:10]:
            categories.append(domain["value"])
            data.append(domain[self.ordering])

        self.build_chart(data, categories, report)
        self.build_detailed_info(domains, report)

    def build_detailed_info(self, domains, report):
        for domain in domains[:self.meta['job']['params']['limit_n_entries']]:
            report.add_header("Domain: %s, Duration: %d, Bandwidth: %d MB" % (domain["value"], domain["duration"], domain["size"] / (1024 * 1024)), H2)
            user_table = [["User", "Duration (sec)", "Bandwidth (MB)"]]
            with open(os.path.join(self.report_directory, 'data', 'domains', str(domain["id"]), 'detailed')) as users_file:
                users = json.load(users_file)
                if users is not None and len(users) != 0:
                    users = users["records"]
                else:
                    continue
                users.sort(key=lambda u: u["size"], reverse=True)
                for user in users[:self.meta['job']['params']['limit_n_drilldown']]:
                    user_table.append([user["value"],user["duration"]/(1000), user["size"] / (1024 * 1024)])
            report.add_table(user_table, [60, 20, 20])

    def build_chart(self, data, categories, report):
        pass

class SquidDomainByBandwidth(SquidDomainReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per Domain (in megabytes)", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)
