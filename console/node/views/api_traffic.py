import os
import json

#
#
#
from _domain.core import Paths
from _domain.utils import FolderInfo

#
#
#
from django.views import generic
from django.http import HttpResponse
from console.settings import DATABASES

#
#
#
from api_system import CommandDiskFree
from api_ps import CommandPs

#
#
#
class ViewApiDashTraffic(generic.View):

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
        data['stats']['dbsize'] = 0
        if DATABASES['monitor']['ENGINE'] == 'django.db.backends.sqlite3':
            data['stats']['dbsize'] = os.path.getsize(DATABASES['monitor']['NAME'])
            data['stats']['dbtype'] = 'sqlite'

        # get processes mysql daemon
        processes = []
        try:
            processes = CommandPs('mysql').run()
        except Exception as e:
            data['error'] = True
            data['desc']  = str(e)

        # see if mysql binary is there and fill the stats
        found = False
        for process in processes:
            if process['path'].find("/mysql") != -1:
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
            data['desc']  = 'the MySQL/MariaDB daemon is not running'

        # add the processes anyway
        data['info']['processes'] = processes

        # and store as array
        return HttpResponse(json.dumps([data], ensure_ascii=True), content_type='application/json')