import os
import json
import subprocess

#
#
#
from _domain.core import Paths, WsUser
from _domain.utils import FolderInfo

#
#
#
from django.views import generic
from django.http import HttpResponse

#
#
#
from api_ps import CommandPs
from api_system import CommandDiskFree
from console.settings import DATABASES

#
#
#
class ViewApiDashWsmgrd(generic.View):

    def get_mysqldb_size(self):

        size = 0
        try:
            uname = DATABASES['monitor']['USER']
            upass = DATABASES['monitor']['PASSWORD']

            args = ["mysql", "-u", uname, "--password=" + upass, "--batch"]
            sql  = "SELECT sum(round(((data_length + index_length)), 2)) FROM information_schema.TABLES WHERE table_schema = 'websafety_monitor'"

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

        return int(size)

    def get(self, request, *args, **kwargs):

        # allocate default response
        data = { 'error' : False, 'desc' : '', 'info' : {}, 'stats' : {} }

        # dump amount of free place
        (success, info) = CommandDiskFree().run(os.path.join(Paths.var_dir(), "monitor"))
        if success:
            disk = {
                'free'  : info['avail'],
                'used'  : info['used'],
                'total' : info['size'],
                'ratio' : info['ratio'].replace('%', '')
            }
            data['stats']['disk'] = disk

        # we also need to know how many files to upload
        data['stats']['queue'] = FolderInfo(os.path.join(Paths.var_dir(), "monitor")).get_size()

        data['stats']['dbtype'] = 'mysql'
        data['stats']['dbsize'] = self.get_mysqldb_size()
        if DATABASES['monitor']['ENGINE'] == 'django.db.backends.sqlite3':
            data['stats']['dbsize'] = os.path.getsize(DATABASES['monitor']['NAME'])
            data['stats']['dbtype'] = 'sqlite'

        # get processes wsmgrd daemon
        processes = []
        try:
            processes = CommandPs(WsUser.name()).run()
        except Exception as e:
            data['error'] = True
            data['desc']  = str(e)

        # see if wsmgrd binary is there and fill the stats
        found = False
        for process in processes:
            if process['path'].find(Paths.bin_dir() + "/wsmgrd") != -1:
                found = True
                data['info']['path']  = process['path']
                data['info']['pid']   = process['pid']
                data['info']['user']   = process['user']
                data['stats']['cpu_time']  = process['cpu_time']
                data['stats']['cpu_usage'] = process['cpu_usage']
                data['stats']['mem_size']  = int(process['mem_size'])
                data['stats']['mem_usage'] = process['mem_usage']

        # no wsmgrd daemon means something is really bad tell the caller
        if not found:
            data['error'] = True
            data['desc']  = 'the wsmgrd daemon is not running'

        # add the processes anyway
        data['info']['processes'] = processes

        # and store as array
        return HttpResponse(json.dumps([data], ensure_ascii=True), content_type='application/json')