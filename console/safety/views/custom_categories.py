import os

#
#
#
from _domain.core import Paths
from _domain.utils import FolderInfo, FileInfo

#
#
#
from django.views import generic

#
#
#
from safety.models import CustomCategory

#
#
#
class CustomCategorySyncer:

    def sync_from_disk(self):

        # we must always sync file system -> table
        dir  = os.path.join(Paths.var_dir(), "spool", "categories_custom")
        list = []
        for sub in os.walk(dir).next()[1]:
            name = sub
            path = os.path.join(dir, sub)
            file = os.path.join(path, "domains")
            if os.path.exists(file):
                list.append({ 'name' : name,  'path' : path })

        # drop existing categories
        CustomCategory.objects.all().delete()

        # upload all new
        for object in list:
            category = CustomCategory()
            category.name          = object['name']
            category.title         = object['name'].title()
            category.description   = "%s, size on disk %s" % (object['path'], FolderInfo(object['path']).get_size())
            category.save()


#
#
#
class ViewCustomCategories(generic.ListView):

    template_name = 'safety/subscriptions/categorycustom_list.html'

    def get_queryset(self):

        # we must always sync file system -> table on every get
        CustomCategorySyncer().sync_from_disk()

        # construct the list
        object_list = []
        for item in CustomCategory.objects.order_by('name'):
            dir      = os.path.join(Paths.var_dir(), "spool", "categories_custom", item.name)
            size     = FolderInfo(dir).get_size()
            modified = FileInfo(os.path.join(dir, "domains")).last_modified()

            object_list.append( {'name':item.name, 'title': item.title, 'dir':dir, 'size':size, 'modified':modified} )

        return object_list