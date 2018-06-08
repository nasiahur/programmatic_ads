import json
import argparse
import logging
import os

from base_report import *

class PolicyReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'policies.json')) as policies_file:
            policies = json.load(policies_file)

        data = []
        categories = []
        for policy in policies:
            categories.append(policy["value"])
            data.append(policy[self.ordering])

        self.build_chart(data, categories, report)
        self.build_detailed_info(policies, report)

    def build_detailed_info(self, policies, report):
        for policy in policies:
            report.add_header("Policy: %s, Requests: %d, Bandwidth: %d MB, Users: %d" % (policy["value"], policy["hits"], policy["size"] / (1024 * 1024), policy["users"]), H2)
            policy_table = [["Users", "Requests", "Bandwidth (MB)"]]
            with open(os.path.join(self.report_directory, 'data', str(policy["id"]), 'users.json')) as policies_file:
                policies = json.load(policies_file)
                for policy in policies:
                    policy_table.append([policy["value"], policy["hits"], policy["size"] / (1024 * 1024)])
            report.add_table(policy_table, [70, 10, 20])

    def build_chart(self, data, categories, report):
        pass


class TopPolicyByRequests(PolicyReport):
    def build_chart(self, data, categories, report):
        report.add_header("Requests per Policy (in thousands)", H2)
        dataLabel = lambda x: str(x / 1000) + "K"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopPolicyByBandwidth(PolicyReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per Policy (in megabytes)", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopPolicyByUsers(PolicyReport):
    def build_chart(self, data, categories, report):
        report.add_header("Users per Policy", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopPolicyByIps(PolicyReport):
    def build_chart(self, data, categories, report):
        report.add_header("IPs per Policy", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)
