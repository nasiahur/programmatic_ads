import os
import datetime
import xml.etree.ElementTree as ET 

#
#
#
from _domain.core import Paths

#
#
#
class DefinitionFile:    

    def get_date(self, current_xml):
        
        if not os.path.exists(current_xml):
            return "File %s does not exist, setting creation date to empty string" % (current_xml)
        
        tree = ET.ElementTree(file=current_xml)
        
        for elem in tree.findall('.//CreationDate'):    
            creation_date = elem.text.strip()
            timestamp     = datetime.datetime.fromtimestamp(int(creation_date))
            return timestamp.strftime('%B %d, %Y at %H:%M:%S')

        return "Creation date is NOT found in XML %s" % (current_xml,)

#
#
#
class DefinitionsFactory:

    def get(self):
        
        f = os.path.join(Paths.var_dir(), "spool")
        d = DefinitionFile()
        info  = {
            'adblock'   : d.get_date(os.path.join(f, "adblock", "current.xml")),
            'privacy'   : d.get_date(os.path.join(f, "privacy", "current.xml")),
            'categories': d.get_date(os.path.join(f, "categories", "current.xml")),
            'youtube'   : d.get_date(os.path.join(f, "youtube", "current.xml")),
            'iwf'       : d.get_date(os.path.join(f, "iwf", "current.xml"))
        }
        return info
