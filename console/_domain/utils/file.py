import os
import time
import shutil

#
#
#
class FileWriter:
    
    def __init__(self, dir):
        
        # debug check
        assert(len(dir)) > 0;
        assert(os.path.exists(dir))
        
        # save the folder name
        self.dir = dir
        
    def write(self, name, data):
    
        # generate
        cur_path = os.path.join(self.dir, name)
        bak_path = os.path.join(self.dir, name + '.bak')
        tmp_path = os.path.join(self.dir, name + '.tmp')

        with open(tmp_path, 'w') as fout:
            fout.write(data)

        if os.path.exists(bak_path):
            os.remove(bak_path)
        
        if os.path.exists(cur_path):
            shutil.move(cur_path, bak_path)
        
        shutil.move(tmp_path, cur_path)


#
#
#
class FileReader:
    def __init__(self, file):
        self.file = file
    def read(self):
        with open(self.file) as fin:
            return fin.read()

#
#
#
class FileInfo:
    def __init__(self, file):
        self.file = file

    def last_modified(self):
        try:
            return time.ctime(os.path.getmtime(self.file))
        except:
            return "N/A"


        
