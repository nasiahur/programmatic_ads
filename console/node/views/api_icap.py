import json

#
#
#
from _domain.core import Paths, WsUser

#
#
#
from django.views import generic
from django.http import HttpResponse

#
#
#
from safety.models import Network
from api_ps import CommandPs
from api_system import CommandDiskFree
from api_netstat import CommandNetstat

#
#
#
class ViewApiDashIcap(generic.View):

    def get(self, request, *args, **kwargs):

        # allocate default response
        data = { 'error' : False, 'desc' : '', 'info' : {}, 'stats' : {} }

        # dump amount of free place
        (success, info) = CommandDiskFree().run(Paths.var_dir())
        if success:
            disk = {
                'free'  : info['avail'],
                'used'  : info['used'],
                'total' : info['size'],
                'ratio' : info['ratio'].replace('%', '')
            }
            data['stats']['disk'] = disk

        # get processes wsicapd daemon
        processes = []
        try:
            processes = CommandPs(WsUser.name()).run()
        except Exception as e:
            data['error'] = True
            data['desc']  = str(e)

        # see if wsicapd binary is there and fill the stats
        found = False
        for process in processes:
            if process['path'].find(Paths.bin_dir() + "/wsicapd") != -1:
                found = True
                data['info']['path']  = process['path']
                data['info']['pid']   = process['pid']
                data['info']['user']   = process['user']
                data['stats']['cpu_time']  = process['cpu_time']
                data['stats']['cpu_usage'] = process['cpu_usage']
                data['stats']['mem_size']  = int(process['mem_size'])
                data['stats']['mem_usage'] = process['mem_usage']

        # no wsicapd daemon means something is really bad tell the caller
        if not found:
            data['error'] = True
            data['desc']  = 'the wsicapd daemon is not running'

        # add the processes anyway
        data['info']['processes'] = processes

        # now read the connections
        connections = []
        try:
            icap_port   = str(Network.objects.first().wsicap_port)
            connections = CommandNetstat().run(icap_port)
        except Exception as e:
            pass

        # add the connections
        data['info']['connections'] = connections

        # and store as array
        return HttpResponse(json.dumps([data], ensure_ascii=True), content_type='application/json')