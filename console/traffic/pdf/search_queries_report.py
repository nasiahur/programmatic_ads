import json
import argparse
import logging
import os

from base_report import *

class UserSearchQueriesReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'users.json')) as users_file:
            users = json.load(users_file)

        report.add_header("User Search Queries (total users: %s)" % len(users), H2)
        user_table = [["User Name", "Queries"]]
        for user in users:
            name = user["name"]
            for query in user["queries"]:            
                user_table.append([name, query.encode("ascii", "replace")])
                name = ""
        report.add_table(user_table, [30, 70])
