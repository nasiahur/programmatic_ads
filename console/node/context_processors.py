from node.models import Node

# 
#
#
def node(request):
    return {
        'node': Node.objects.first()
    }