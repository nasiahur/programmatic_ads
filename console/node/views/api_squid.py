import json

#
#
#
from _domain.core import Paths
from _domain.squid import BinarySquid

#
# django
#
from django.views import generic
from django.http import HttpResponse

#
#
#
from api_ps import CommandPs

#
#
#
class ViewApiDashSquid(generic.View):

    def get_settings(self):

        name = os.path.join(Paths.etc_dir(), "system.json")
        with open(name) as fin:    
            data = json.load(fin)

        return data

    def squid_exe_found(self, line):

        if line.find("squid-1") != -1:
            return True

        full_path = BinarySquid.full_path()
        if line.find(full_path) != -1:
            return True

        return False

    def get(self, request, *args, **kwargs):

        # allocate default response
        data = { 'error' : False, 'desc' : '', 'info' : {}, 'stats' : {}, 'runtime' : {} }

        # get processes of squid daemon
        processes = []
        try:
            processes = CommandPs(BinarySquid.runas_user()).run()
        except Exception as e:
            data['error'] = True
            data['desc']  = str(e)

        # for squid we must manually calculate the memory usage
        total_mem_ratio = 0.0
        total_mem_size  = 0
        total_cpu_ratio = 0.0

        for process in processes:
            total_mem_size  += int(process['mem_size'])
            total_mem_ratio += float(process['mem_usage'])
            total_cpu_ratio += float(process['cpu_usage'])

        # see if squid binary is there and fill the stats
        found = False
        for process in processes:
            if self.squid_exe_found(process['path']):
                found = True
                data['info']['path']  = process['path']
                data['info']['pid']   = process['pid']
                data['info']['user']   = process['user']
                data['stats']['cpu_time']  = process['cpu_time']
                data['stats']['cpu_usage'] = str(total_cpu_ratio)
                data['stats']['mem_size']  = total_mem_size
                data['stats']['mem_usage'] = str(total_mem_ratio)

        # no squid daemon means something is really bad tell the caller
        if not found:
            data['error'] = True
            data['desc']  = 'the Squid proxy is not running'

        # add the processes anyway
        data['info']['processes'] = processes

        # and store as array
        return HttpResponse(json.dumps([data], ensure_ascii=True), content_type='application/json')