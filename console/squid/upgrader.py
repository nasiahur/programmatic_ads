import os

#
#
#
from _domain.utils import read_json_array, read_json_object

#
#
#
from squid.models import *

#
#
#
def load_array(conf_file):
    result = []
    with open(conf_file) as fin:
        for line in fin.readlines():
            pos = line.find('#')
            if pos != -1:
                line = line[:pos]
            line = line.strip()

            if len(line) > 0:
                result.append(line)

    return result

#
#
#
def load_payload(conf_file):

    # read all lines into memory
    lines = []
    with open(conf_file) as f:
        lines = f.readlines()

    # throw away any non generated lines
    content = []
    found   = False
    seen    = False

    for line in lines:

        if not found:
            if line.find("-----BEGIN GENERATED CONFIGURATION-----") != -1:
                found = True
                seen  = True
        else:
            if line.find("-----END GENERATED CONFIGURATION-----") != -1:
                found = False
            else:
                content.append(line.strip())

    # and return nicely
    return content





#
#
#
def load_annotated_array(conf_file):

    # read all lines into memory
    lines = []
    with open(conf_file) as f:
        lines = f.readlines()

    # throw away any non generated lines
    content = []
    found   = False
    seen    = False

    for line in lines:

        if not found:
            if line.find("-----BEGIN GENERATED CONFIGURATION-----") != -1:
                found = True
                seen  = True
        else:
            if line.find("-----END GENERATED CONFIGURATION-----") != -1:
                found = False
            else:
                content.append(line.strip())

    # this is the result to be returned
    result = []

    # see if have at least seen our generated config
    if not seen:

        # ok this must be old style generated config, so just load valid lines skipping comments
        for line in load_array(conf_file):
            if len(line) > 0:
                result.append( (line, "") )

        return result

    # if we got here we have nice lines in content to be imported
    comment = ""
    value   = ""
    
    while len(content) > 0:
        item = content.pop(0).strip()
        if item.startswith("#"):
            comment += item.lstrip('#').rstrip('\r\n').strip()
            comment += "\n"
        else:
            value = item

            if len(value) > 0:
                result.append( (value, comment) )

            comment = ""
            value   = ""

    # and return nicely
    return result


#
# special storage for 3.1 and 3.2 types of configuration
#
class Storage:

    def __init__(self, lines):

        self.values = []
        for line in lines:
            try:
                n,v = line.split('=')
                n   = n.strip()
                v   = v.strip()
                if len(n) > 0:
                    self.values.append( (n, v) )
            except:
                pass

    def get_string(self, name):
        for (n,v) in self.values:
            if n.lower() == name.lower():
                return v
        return ""

    def get_int(self, name):
        v = self.get_string(name)
        if v == "":
            return 0
        return int(v)

    def get_bool(self, name):
        v = self.get_string(name).lower() 
        if v == "yes" or v == "on" or v == "true":
            return True
        return False

    def get_list(self, name):
        r = []
        for (n,v) in self.values:
            if n.lower() == name.lower():
                r.append(v)
        return r

#
#
#
class ConfFileReader:

    def __init__(self, path):
        self.path = path

    def read_lines(self, skip_comments):
        lines = self.read_contents(self.path)
        if not skip_comments:
            return lines

        return self.remove_comments(lines)

    def read_contents(self, path):
        with open(self.path) as fin:
            return fin.read().splitlines()

    def remove_comments(self, lines):
        result = []
        for line in lines:    
            pos = line.find('#')
            if pos != -1:
                line = line[0:pos]
            line = line.strip()
            if len(line) > 0:
                result.append(line)
        return result

#
#
#
class SquidImporter:

    def upgrade(self, version, folder):

        #self.upgrade_wsicapd(version, folder)
        self.upgrade_icap(folder)
        self.upgrade_ssl(folder)
        self.upgrade_auth(folder)
        self.upgrade_auth_schemes(version, folder)
        self.upgrade_cache(folder)
        self.upgrade_urlrewrite(folder)

    def upgrade_icap(self, folder):

        # upgrade advanced first
        if True:

            advanced_path = os.path.join(folder, 'adaptation/exclude/advanced.conf')
            if not os.path.isfile(advanced_path):
                advanced_path = os.path.join(folder, 'icap_exclude_advanced.conf')

            if os.path.isfile(advanced_path):

                advanced_data = load_payload(advanced_path)
                advanced_obj  = ExcludeAdvanced.objects.first()
                advanced_obj.value_adaptation = "\n".join(advanced_data)
                advanced_obj.save()
                
        # names to set map
        for name, s in {

            'icap_exclude_content_type.conf'        : ExcludeContentType.objects,
            'adaptation/exclude/content_type.conf'  : ExcludeContentType.objects,

            'icap_exclude_domain_ip4.conf'          : ExcludeDomainIp.objects,
            'icap_exclude_domain_ip6.conf'          : ExcludeDomainIp.objects,
            'adaptation/exclude/domain_ip.conf'     : ExcludeDomainIp.objects,

            'icap_exclude_domain_name.conf'         : ExcludeDomainName.objects,
            'adaptation/exclude/domain_name.conf'   : ExcludeDomainName.objects,

            'icap_exclude_domain_range4.conf'       : ExcludeDomainRange.objects,
            'icap_exclude_domain_range6.conf'       : ExcludeDomainRange.objects,
            'adaptation/exclude/domain_range.conf'  : ExcludeDomainRange.objects,

            'icap_exclude_domain_subnet4.conf'      : ExcludeDomainSubnet.objects,
            'icap_exclude_domain_subnet6.conf'      : ExcludeDomainSubnet.objects,
            'adaptation/exclude/domain_subnet.conf' : ExcludeDomainSubnet.objects,

            'icap_exclude_schedule.conf'            : ExcludeSchedule.objects,
            'adaptation/exclude/schedule.conf'      : ExcludeSchedule.objects,

            'icap_exclude_user_agent.conf'          : ExcludeUserAgent.objects,
            'adaptation/exclude/user_agent.conf'    : ExcludeUserAgent.objects,

            'icap_exclude_user_ip4.conf'            : ExcludeUserIp.objects,
            'icap_exclude_user_ip6.conf'            : ExcludeUserIp.objects,
            'adaptation/exclude/user_ip.conf'       : ExcludeUserIp.objects,

            'icap_exclude_user_name.conf'           : ExcludeUserName.objects,

            'icap_exclude_user_range4.conf'         : ExcludeUserRange.objects,
            'icap_exclude_user_range6.conf'         : ExcludeUserRange.objects,
            'adaptation/exclude/user_range.conf'    : ExcludeUserRange.objects,

            'icap_exclude_user_subnet4.conf'        : ExcludeUserSubnet.objects,
            'icap_exclude_user_subnet6.conf'        : ExcludeUserSubnet.objects,
            'adaptation/exclude/user_subnet.conf'   : ExcludeUserSubnet.objects
        }.iteritems():

            # load file contents as array
            path1 = os.path.join(folder, name)
            if os.path.exists(path1):
                for (value, comment) in load_annotated_array(path1):
                    try:
                        v, c = s.get_or_create(value=value)
                        v.comment           = comment
                        v.bypass_adaptation = True
                        v.save()
                    except Exception as e:
                        # logging.warning("Ignoring import of %s, error '%s' ..." % (value, str(e)))
                        pass

    def upgrade_cache(self, folder):

        # upgrade advanced first
        if True:

            advanced_path = os.path.join(folder, 'cache/exclude/advanced.conf')            
            if os.path.isfile(advanced_path):

                advanced_data = load_payload(advanced_path)
                advanced_obj = ExcludeAdvanced.objects.first()
                advanced_obj.value_cache = "\n".join(advanced_data)
                advanced_obj.save()
                
        # names to set map
        for name, s in {

            'cache/exclude/content_type.conf'  : ExcludeContentType.objects,
            'cache/exclude/domain_ip.conf'     : ExcludeDomainIp.objects,
            'cache/exclude/domain_name.conf'   : ExcludeDomainName.objects,
            'cache/exclude/domain_range.conf'  : ExcludeDomainRange.objects,
            'cache/exclude/domain_subnet.conf' : ExcludeDomainSubnet.objects,
            'cache/exclude/schedule.conf'      : ExcludeSchedule.objects,
            'cache/exclude/user_agent.conf'    : ExcludeUserAgent.objects,
            'cache/exclude/user_ip.conf'       : ExcludeUserIp.objects,
            'cache/exclude/user_name.conf'     : ExcludeUserName.objects,
            'cache/exclude/user_range.conf'    : ExcludeUserRange.objects,
            'cache/exclude/user_subnet.conf'   : ExcludeUserSubnet.objects
        }.iteritems():

            # load file contents as array
            path1 = os.path.join(folder, name)
            if os.path.exists(path1):
                for (value, comment) in load_annotated_array(path1):
                    try:
                        v, c = s.get_or_create(value=value)
                        v.bypass_cache = True
                        v.comment      = comment
                        v.save()
                    except Exception as e:
                        # logging.warning("Ignoring import of %s, error '%s' ..." % (value, str(e)))
                        pass

    def upgrade_urlrewrite(self, folder):

        # upgrade advanced first
        if True:

            advanced_path = os.path.join(folder, 'urlrewrite/exclude/advanced.conf')
            if os.path.isfile(advanced_path):
                advanced_data = load_payload(advanced_path)
                advanced_obj = ExcludeAdvanced.objects.first()
                advanced_obj.value_urlrewrite = "\n".join(advanced_data)
                advanced_obj.save()

        # names to set map
        for name, s in {

            'urlrewrite/exclude/domain_ip.conf': ExcludeDomainIp.objects,
            'urlrewrite/exclude/domain_name.conf': ExcludeDomainName.objects,
            'urlrewrite/exclude/domain_range.conf': ExcludeDomainRange.objects,
            'urlrewrite/exclude/domain_subnet.conf': ExcludeDomainSubnet.objects,
            'urlrewrite/exclude/schedule.conf': ExcludeSchedule.objects,
            'urlrewrite/exclude/user_agent.conf': ExcludeUserAgent.objects,
            'urlrewrite/exclude/user_ip.conf': ExcludeUserIp.objects,
            'urlrewrite/exclude/user_name.conf': ExcludeUserName.objects,
            'urlrewrite/exclude/user_range.conf': ExcludeUserRange.objects,
            'urlrewrite/exclude/user_subnet.conf': ExcludeUserSubnet.objects
        }.iteritems():

            # load file contents as array
            path1 = os.path.join(folder, name)
            if os.path.exists(path1):
                for (value, comment) in load_annotated_array(path1):
                    try:
                        v, c = s.get_or_create(value=value)
                        v.bypass_urlrewrite = True
                        v.comment = comment
                        v.save()
                    except Exception as e:
                        # logging.warning("Ignoring import of %s, error '%s' ..." % (value, str(e)))
                        pass

    def upgrade_ssl(self, folder):

        # upgrade advanced first
        if True:

            advanced_path = os.path.join(folder, 'ssl/exclude/advanced.conf')
            if os.path.isfile(advanced_path):

                advanced_data = load_payload(advanced_path)
                advanced_obj  = ExcludeAdvanced.objects.first()
                advanced_obj.value_ssbump = "\n".join(advanced_data)
                advanced_obj.save()

        # upgrade NON bumped categories
        if True:

            path = os.path.join(os.path.dirname(folder), "safety", "non_bumped_categories.json")
            if os.path.exists(path):

                obj     = ExcludeCategories.objects.first()
                entries = read_json_array(path)
                for entry in entries:

                    attrname = "exclude_%s" % entry
                    setattr(obj, attrname, True)

                obj.save()

        # upgrade ssl exclusions
        for name, s in {
            'https_exclusions.conf':    ExcludeDomainName.objects,
            'ssl_exclude_domains.conf': ExcludeDomainName.objects,
            'ssl/exclude/domains.conf': ExcludeDomainName.objects,
            'ssl_exclude_ips.conf':     ExcludeDomainIp.objects,
            'ssl/exclude/ips.conf':     ExcludeDomainIp.objects,
            'ssl_exclude_subnets.conf': ExcludeDomainSubnet.objects,
            'ssl/exclude/subnets.conf': ExcludeDomainSubnet.objects,
        }.iteritems():

            # load file contents as array
            path1 = os.path.join(folder, name)
            if os.path.exists(path1):
                for (value, comment) in load_annotated_array(path1):
                    try:
                        v, c = s.get_or_create(value=value)
                        v.bypass_sslbump = True
                        v.comment        = comment
                        v.save()
                    except Exception as e:
                        # logging.warning("Ignoring import of %s, error '%s' ..." % (value, str(e)))
                        pass

        # name to set map
        for name, s in {
            'https_targets.conf'       : SslTargetDomain.objects,
            'ssl_target_domains.conf'  : SslTargetDomain.objects,
            'ssl/target/domains.conf'  : SslTargetDomain.objects,
            'ssl_target_ips.conf'      : SslTargetIp.objects,
            'ssl/target/ips.conf'      : SslTargetIp.objects,
            'ssl_target_subnets.conf'  : SslTargetSubnet.objects,
            'ssl/target/subnets.conf'  : SslTargetSubnet.objects,
            'ssl_error_domains.conf'   : SslErrorDomain.objects,
            'ssl/error/domains.conf'   : SslErrorDomain.objects,
            'ssl_error_ips.conf'       : SslErrorIp.objects,
            'ssl/error/ips.conf'       : SslErrorIp.objects,
            'ssl_error_subnets.conf'   : SslErrorSubnet.objects,
            'ssl/error/subnets.conf'   : SslErrorSubnet.objects

        }.iteritems():

            # load file contents as array
            path1 = os.path.join(folder, name)
            if os.path.exists(path1):
                for (value, comment) in load_annotated_array(path1):
                    try:
                        v, c = s.get_or_create(value=value)
                        v.comment = comment
                        v.save()
                    except Exception as e:
                        # logging.warning("Ignoring import of %s, error '%s' ..." % (value, str(e)))
                        pass

        # we cannot automatically enable bump mode, admin needs to do it explicitly


    def upgrade_auth(self, folder):

        # upgrade advanced first
        if True:

            advanced_path = os.path.join(folder, 'authentication/exclude/advanced.conf')
            if not os.path.isfile(advanced_path):
                advanced_path = os.path.join(folder, 'auth_exclude_advanced.conf')

            if os.path.isfile(advanced_path):

                advanced_data = load_payload(advanced_path)
                advanced_obj = ExcludeAdvanced.objects.first()
                advanced_obj.value_auth = "\n".join(advanced_data)
                advanced_obj.save()

        # name to set map
        for name, s in {
            
            'auth_exclude_domain_ip4.conf'              : ExcludeDomainIp.objects,
            'auth_exclude_domain_ip6.conf'              : ExcludeDomainIp.objects,
            'authentication/exclude/domain_ip.conf'     : ExcludeDomainIp.objects,
            'auth_exclude_domain_name.conf'             : ExcludeDomainName.objects,
            'authentication/exclude/domain_name.conf'   : ExcludeDomainName.objects,
            'auth_exclude_domain_range4.conf'           : ExcludeDomainRange.objects,
            'auth_exclude_domain_range6.conf'           : ExcludeDomainRange.objects,
            'authentication/exclude/domain_range.conf'  : ExcludeDomainRange.objects,
            'auth_exclude_domain_subnet4.conf'          : ExcludeDomainSubnet.objects,
            'auth_exclude_domain_subnet6.conf'          : ExcludeDomainSubnet.objects,
            'authentication/exclude/domain_subnet.conf' : ExcludeDomainSubnet.objects,
            'auth_exclude_schedule.conf'                : ExcludeSchedule.objects,
            'authentication/exclude/schedule.conf'      : ExcludeSchedule.objects,
            'auth_exclude_user_agent.conf'              : ExcludeUserAgent.objects,
            'authentication/exclude/user_agent.conf'    : ExcludeUserAgent.objects,
            'auth_exclude_user_ip4.conf'                : ExcludeUserIp.objects,
            'auth_exclude_user_ip6.conf'                : ExcludeUserIp.objects,
            'authentication/exclude/user_ip.conf'       : ExcludeUserIp.objects,
            'auth_exclude_user_range4.conf'             : ExcludeUserRange.objects,
            'auth_exclude_user_range6.conf'             : ExcludeUserRange.objects,
            'authentication/exclude/user_range.conf'    : ExcludeUserRange.objects,
            'auth_exclude_user_subnet4.conf'            : ExcludeUserSubnet.objects,
            'auth_exclude_user_subnet6.conf'            : ExcludeUserSubnet.objects,
            'authentication/exclude/user_subnet.conf'   : ExcludeUserSubnet.objects
        }.iteritems():

            # load file contents as array
            path1 = os.path.join(folder, name)
            if os.path.exists(path1):
                for (value, comment) in load_annotated_array(path1):
                    try:
                        v, c = s.get_or_create(value=value)
                        v.bypass_auth = True
                        v.comment     = comment
                        v.save()
                    except Exception as e:
                        # logging.warning("Ignoring import of %s, error '%s' ..." % (value, str(e)))
                        pass

    def upgrade_auth_schemes(self, version, folder):

        file = os.path.join(folder, "auth_labels.json")
        if not os.path.isfile(file):
            return

        data = read_json_object(file)

        # save labelling
        obj        = AuthLabel.objects.first()
        obj.enable = data['enable']
        obj.resolve_ip_as_user_name = data['resolve_ip_as_user_name']        
        obj.save()

        # save labels
        for label in data["labels"]:

            if not label["user_name"]:
                continue

            try:
                v, c = AuthLabelUsers.objects.get_or_create(user_name=label["user_name"])
                v.user_ip  = label["user_ip"]
                v.user_mac = label["user_eui"]
                v.comment  = label["comment"]
                
                v.save()
            except Exception as e:
                #logging.warning("Ignoring import of user name label %s, error '%s' ..." % (label["user_name"], str(e)))
                pass

#
#
#
class Upgrader(object):

    def __init__(self, major, minor):

        self.major   = major
        self.minor   = minor

    def upgrade(self, etc_dir):

    	SquidImporter().upgrade( "%d.%d" % (self.major, self.minor), os.path.join(etc_dir, "squid"))