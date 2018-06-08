import json
import argparse
import logging
import os

from base_report import *

class IpReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'ips.json')) as ips_file:
            ips = json.load(ips_file)

        data = []
        categories = []
        for ip in ips[:10]:
            categories.append(ip["value"])
            data.append(ip[self.ordering])

        self.build_chart(data, categories, report)
        self.build_detailed_info(ips, report)

    def build_detailed_info(self, ips, report):
        for ip in ips:
            report.add_header("IP: %s, Requests: %d, Bandwidth: %d MB, Domains: %d" % (ip["value"], ip["hits"], ip["size"] / (1024 * 1024), ip["domains"]), H2)
            ip_table = [["Visited domains", "Requests", "Bandwidth (MB)"]]
            with open(os.path.join(self.report_directory, 'data', str(ip["id"]), 'domains.json')) as domains_file:
                domains = json.load(domains_file)
                for domain in domains:
                    ip_table.append([domain["value"], domain["hits"], domain["size"] / (1024 * 1024)])
            report.add_table(ip_table, [70, 10, 20])

    def build_chart(self, data, categories, report):
        pass


class TopIpByRequests(IpReport):
    def build_chart(self, data, categories, report):
        report.add_header("Requests per IP (in thousands)", H2)
        dataLabel = lambda x: str(x / 1000) + "K"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopIpByBandwidth(IpReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per IP (in megabytes)", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopIpByDomains(IpReport):
    def build_chart(self, data, categories, report):
        report.add_header("Domains per IP (in hundreds)", H2)
        dataLabel = lambda x: str(x / 100) + "H"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopIpByBlockedDomains(IpReport):
    def build_chart(self, data, categories, report):
        report.add_header("Domains per IP", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)







