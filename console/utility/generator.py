#
# system
#
import os
import shutil

#
#
#
class BaseGenerator(object):

    #
    #
    #
    def __init__(self, root_dir):
        self.root_dir = root_dir

    #
    #
    #
    def generate(self):

        # construct dirs
        cur_dir = self.root_dir
        new_dir = self.root_dir + ".new"
        bak_dir = self.root_dir + ".bak"
        
        # recreate new dir
        self.recreate_dir(new_dir)

        # generate all config into new dir
        self.generate_config(new_dir)

        # backup current dir
        if os.path.exists(cur_dir):
            
            # remove backup dir
            if os.path.exists(bak_dir):
                shutil.rmtree(bak_dir)

            # and move current into bak
            shutil.copytree(cur_dir, bak_dir)            
            shutil.rmtree(cur_dir)

        # move new into current
        shutil.move(new_dir, cur_dir)

    #
    #
    #
    def recreate_dir(self, dir_name):

        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)