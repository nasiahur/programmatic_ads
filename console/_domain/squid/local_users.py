import os
import json

#
# 
#
from _domain.core import Paths
from _domain.utils import FileWriter, JsonDumper

#
#
#
from htpasswd import CommandHtPasswd


#
#
#
class LocalUsers:

    def __init__(self):

        self.etc_dir  = Paths.etc_dir()
        self.database = os.path.join(self.etc_dir, "users.htpasswd")
        self.json     = os.path.join(self.etc_dir, "users.json")

    def exists(self):

        if os.path.exists(self.database):
            return True
        return False

    def get_comments(self):

        comments = {}
        name     = self.json
        if os.path.exists(name):
            with open(name) as fin:    
                comments = json.load(fin)

        return comments

    def get_users(self):

        # first read the comments
        comments = self.get_comments()
        
        # now list the actual user names
        array = []
        name  = self.database

        if os.path.exists(name):

            with open(name, "r") as fin:
                entries = fin.readlines()

                for entry in entries:
                    pos = entry.find(":")
                    if pos != -1:

                        user    = entry[0:pos]
                        encpass = entry[pos + 1:].strip().strip('\r').strip('\n').strip()
                        comment = ""
                        if user in comments:
                            comment = comments[user]['comment']

                        array.append( {
                            "pk"      : user,
                            "user"    : user,
                            "encpass" : encpass,
                            "comment" : comment
                        })

        # and return nicely
        return array

    def get_user(self, name):
        entries = self.get_users()
        for entry in entries:
            if entry['user'] == name:
                return entry
        return None

    def delete_user(self, name):

        CommandHtPasswd(self.database).delete_user(name)

    def create_user(self, username, pasw, comment):

        # create the user in htpasswd file
        CommandHtPasswd(self.database).create_user(username, pasw)

        # if we got here then the user was created, add the comment to the users.json file
        self.update_comment(username, comment)
        
    def update_comment(self, username, comment):
        
        data = {}
        name = self.json
        if os.path.exists(name):
            with open(name) as fin:    
                data = json.load(fin)

        data[username] = {
            "comment" : comment
        }

        # and save it
        w = FileWriter(self.etc_dir)
        d = JsonDumper()

        w.write("users.json", d.dumps(data))


#
# test some stuff
#
if __name__ == "__main__":

    db = LocalUsers(r"m:\websafety\tools\test-var\htpasswd")
    db.exists()

    comments = db.get_comments()
    users    = db.get_users()

    john = db.get_user("john.rambo")
    if john is not None:
        db.delete_user(john['user'])

    db.create_user("john.rambo", "Passw0rd", "This is John")

    john = db.get_user("john.rambo")
    assert(john is not None)
