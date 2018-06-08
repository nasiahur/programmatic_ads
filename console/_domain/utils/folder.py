import os

#
#
#
class FolderInfo:
    
    def __init__(self, folder):
        self.folder = folder
        
    def get_size(self):
        return self.get_size_internal(self.folder)
        
    def get_size_internal(self, path):

        # see if the passed in name is a file
        if os.path.isfile(path):
            return long(os.path.getsize(path))
        elif not os.path.isdir(path):
            return long(0)
        else:
            # ok this is a folder, enumerate it
            total = long(0)
            for item in os.listdir(path):
                newpath = os.path.join(path, item)
                current = self.get_size_internal(newpath)
                total  += current
                
            return long(total)