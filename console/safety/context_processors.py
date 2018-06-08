from _domain.core  import Distrib
from safety.models import Safety

# 
#
#
def safety(request):
    return {
        'safety': Safety.objects.first()
    }

