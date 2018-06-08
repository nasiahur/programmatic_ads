import re
import json
import datetime
import multiprocessing

#
# business logic
#
from _domain.squid import LdapDetector, SquidClient
from _domain.node import TimeZone

#
# django
#
from django.views import generic
from django.http import HttpResponse

#
#
#
from timezone import TimeZoneReboot
from api_system import SystemInfo, Uptime, CommandCpuUsage
from api_memory import Memory, Swap
from squid.models import Network, AuthAd
from console.settings import DATABASES, LANGUAGE_CODE, TIME_ZONE, USE_TZ


#
#
#
class ViewApiDashInfo(generic.View):

    def get(self, request, *args, **kwargs):

        # get time information
        (utcnow_ad_str, utcnow_drift) = self.get_adutctime()

        # time difference between UTC on this proxy box and on DC is dangerous if it is > 5 minutes
        # in this case Kerberos auth will always fail!!!
        utcnow_drift_dangerous = False
        if utcnow_drift > 5:
            utcnow_drift_dangerous = True

        # get the system time zone and reboot required attribute
        timezone_running  = self.get_systimezone()
        timezone_django   = self.get_djangotimezone()
        timezone_unsynced = TimeZoneReboot().required or (not timezone_running.startswith(timezone_django))

        s = SystemInfo()
        data = [{
            'error' : False,
            'info'  : {
                'hostname': s.get_hostname(),
                'ips': s.get_nics(),
                'os': s.get_info(),
                'arch': s.get_arch(),
                'cpus': multiprocessing.cpu_count(),
                'uptime': Uptime().get(),
                'memory' : Memory().get(),
                'swap' : Swap().get(),
                'cpu_usage' : str(CommandCpuUsage().run()),
                'python' : s.get_pythonver(),
                'timezone' : timezone_running,
                'timezone_django'   : timezone_django,
                'django_use_tz'     : USE_TZ,
                'timezone_unsynced' : timezone_unsynced,
                'locale': LANGUAGE_CODE,
                'localtime': str(datetime.datetime.now()),
                'utctime': str(datetime.datetime.utcnow()),
                'utcnow_ad_str' : utcnow_ad_str,
                'utcnow_drift' : utcnow_drift,
                'utcnow_drift_dangerous' : utcnow_drift_dangerous
            }
        }]

        return HttpResponse(json.dumps(data, ensure_ascii=True), content_type='application/json')

    def get_systimezone(self):

        value = ""

        try:
            value = TimeZone().running_tz_str()                
        except Exception as e:
            value = str(e)            
        return value

    def get_djangotimezone(self):
        return TIME_ZONE


    def get_adutctime(self):

        utcnow_ad_str = ""
        utcnow_drift  = 0 # in minutes

        try:
            # dc1
            dc1addr = AuthAd.objects.first().dc1addr
            if len(dc1addr) > 0:

                (defaultNamingContext, currentTimeList) = LdapDetector().inspect_rootdse(dc1addr)

                if len(currentTimeList) == 1:

                    currentTime = currentTimeList[0]
                    if currentTime != "":

                        # parse current time in datetime object
                        utcnow_ad   = datetime.datetime.strptime(currentTime, "%Y%m%d%H%M%S.%fZ")

                        # get the UTC time on this proxybox (host)
                        utcnow_host = datetime.datetime.utcnow()

                        # check if these are within 5 minutes
                        utcnow_drift = utcnow_ad - utcnow_host

                        # total seconds need to be int to be correctly devided by 60
                        (quotient, remainder) = divmod(int(utcnow_drift.total_seconds()), 60)

                        # save the values
                        utcnow_ad_str = utcnow_ad.strftime("%Y-%m-%d %H:%M:%S.%fZ")
                        utcnow_drift  = quotient

        except Exception as e:
            print str(e)

        return (utcnow_ad_str, utcnow_drift)




#
#
#
class ViewApiDashSquidRuntime(generic.View):

    def get(self, request, *args, **kwargs):

        data = { 'info' : {} }

        try:

            network = Network.objects.first()

            client  = SquidClient(network.explicit_address, network.explicit_port)
            lines   = client.mrginfo_str().split("\n")

            for line in lines:

                match = re.match( r'\sCPU\sUsage\:\s+(.*)%', line, re.M|re.I)
                if match:
                    data['info']['CPUUsage'] = float(match.group(1))
                    
                match = re.match( r'\s*Number\sof\sfile\sdesc\scurrently\sin\suse:\s+(.*)', line, re.M|re.I)
                if match:
                    data['info']['UsedFileDescriptors'] = int(match.group(1))

                match = re.match( r'\s*Available\snumber\sof\sfile\sdescriptors:\s+(.*)', line, re.M|re.I)
                if match:
                    data['info']['AvailableNumberOfFileDescriptors'] = int(match.group(1))

                match = re.match( r'\s*Number\sof\sclients\saccessing\scache:\s+(.*)', line, re.M|re.I)
                if match:
                    data['info']['NumberOfClients'] = int(match.group(1))

                match = re.match( r'\s*Number\sof\sHTTP\srequests\sreceived:\s+(.*)', line, re.M|re.I)
                if match:
                    data['info']['HttpRequestsReceived'] = int(match.group(1))

                match = re.match( r'\s*Average\sHTTP\srequests\sper\sminute\ssince\sstart:\s+(.*)', line, re.M|re.I)
                if match:
                    data['info']['AvgHttpRequestsPerMinuteSinceStart'] = float(match.group(1))

                match = re.match( r'\sDNS\sLookups\:\s+([\d\.]+)\s(.*)', line, re.M|re.I)
                if match:
                    data['info']['DnsLookup5Min'] = float(match.group(1))
                    data['info']['DnsLookup60Min'] = float(match.group(2))
                    
        except Exception as e:

            data['error'] = True
            data['desc']  = str(e)

        return HttpResponse(json.dumps([data], ensure_ascii=True), content_type='application/json')
