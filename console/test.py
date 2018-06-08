#!/usr/bin/env python
import os
import sys
import datetime
import django

sys.path.append(os.path.abspath(__file__))


if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "console.settings")
    
    # dirty fix
    size = 0
    try:
        import subprocess
    
        args = ["mysql", "-u", "root", "--password=Passw0rd", "--batch"]
        sql  = "SELECT sum(round(((data_length + index_length)), 2)) FROM information_schema.TABLES WHERE table_schema = 'qlproxy_monitor'"

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        # wait until it is finished
        (stdout, stderr) = process.communicate(input=sql)

        # and return
        if process.returncode != 0:
            raise Exception(stderr)
        
        value = '0'
        lines = stdout.split('\n')
        for line in lines:
            if len(line) == 0:
                continue    
            if line.find('sum(round') != -1:
                continue
            value = line
            break;
        size = float(value)
    except Exception as e:
        pass

    print size
    #return 1000000

    from django.contrib.auth import authenticate
    from django.db import connection
    from diladele.generator import Generator
    from diladele.models import *
    from diladele.folder import FolderInfo    
    from qlproxy.models import *
    from squid.models import *
    from report.models import *



    
    # add the top level objecti
    # for mysql we ask it directly
    try:
        #context['db_size'] = 0

        d = datetime.datetime.strptime('2012-03-01T10:00:00Z','%Y-%m-%dT%H:%M:%SZ')
        print d

        #cursor = connection.cursor()
        #cursor.execute("SELECT sum(round(((data_length + index_length) / 1024 / 1024 / 1024), 2))  as 'Size in GB' FROM information_schema.TABLES WHERE table_schema = 'qlproxy_monitor'")
        #row = cursor.fetchone()
        #context['db_size'] = row[0]
    except Exception as e:
        print e
