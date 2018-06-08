import json
import argparse
import logging
import os
import datetime

from base_report import *

class YoutubeReport(BaseReport):
    def build_content(self, report):

        with open(os.path.join(self.report_directory, 'data', 'users.json')) as users_file:
            users = json.load(users_file)

        report.add_header("User Youtube Videos (total users: %s)" % len(users), H2)
        user_table = [["User Name", "Video", "Timestamp"]]
        for user in users:
            name = user["name"]
            videos = user["videos"]
            for video in videos:
                title = video["title"]
                title = '<a color="blue" href="http://youtube.com/watch?' + video["url"] + '">' + title + '</a>'
                stamp = datetime.datetime.strptime(video["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
                user_table.append([name, Paragraph(title, report.theme.paragraph), stamp])
                name = ""
        report.add_table(user_table, [25, 55, 20])
