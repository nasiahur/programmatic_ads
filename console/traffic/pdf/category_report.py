import json
import argparse
import logging
import os

from base_report import *

class CategoryReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'categories.json')) as categories_file:
            categories = json.load(categories_file)

        data = []
        cats = []
        for category in categories[:10]:
            cats.append(category["value"])
            data.append(category[self.ordering])

        self.build_chart(data, cats, report)
        self.build_detailed_info(categories, report)

    def build_detailed_info(self, categories, report):
        for category in categories:
            report.add_header("Category: %s, Requests: %d, Bandwidth: %d MB, Users: %d" % (category["value"], category["hits"], category["size"] / (1024 * 1024), category["users"]), H2)
            category_table = [["Users", "Requests", "Bandwidth (MB)"]]
            with open(os.path.join(self.report_directory, 'data', str(category["id"]), 'users.json')) as users_file:
                users = json.load(users_file)
                for user in users:
                    category_table.append([user["value"], user["hits"], user["size"] / (1024 * 1024)])
            report.add_table(category_table, [70, 10, 20])

    def build_chart(self, data, categories, report):
        pass


class TopCategoryByRequests(CategoryReport):
    def build_chart(self, data, categories, report):
        report.add_header("Requests per Category (in thousands)", H2)
        dataLabel = lambda x: str(x / 1000) + "K"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopCategoryByBandwidth(CategoryReport):
    def build_chart(self, data, categories, report):
        report.add_header("Bandwidth per Category (in megabytes)", H2)
        dataLabel = lambda x: str(x / (1024 * 1024)) + "MB"
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopCategoryByUsers(CategoryReport):
    def build_chart(self, data, categories, report):
        report.add_header("Users per Category", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)

class TopCategoryByIps(CategoryReport):
    def build_chart(self, data, categories, report):
        report.add_header("IPs per Category", H2)
        dataLabel = lambda x: str(x)
        report.add_vertical_bar_chart(data, categories, dataLabel)
