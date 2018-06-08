from _domain.core import Distrib
# 
#
#
def is_pfsense(request):

    is_pfsense = False
    if Distrib.WS_PFSENSE == Distrib.name():
        is_pfsense = True

    return {
        'is_pfsense': is_pfsense
    }