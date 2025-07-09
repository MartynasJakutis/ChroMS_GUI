from os.path import (join as os_path_join,
                     abspath as os_path_abspath,
                     dirname as os_path_dirname,
                     isdir as os_path_isdir)
from os import (listdir as os_listdir,
                mkdir as os_mkdir,
                sep as os_sep)

os_dir_separator = os_sep

def get_absolute_script_path(file = __file__, output_parent_dir = True):
    file_abspath = os_path_abspath(file)
    folder_abspath = os_path_dirname(file_abspath)
    if not output_parent_dir:
        return folder_abspath
    else:
        parent_dir_abspath = os_path_dirname(folder_abspath)
        return parent_dir_abspath

def get_path(folder, file):
    """Returns path consisting of folder and file. folder, file - str."""
    return os_path_join(folder, file)

def create_dir_if_not_present(dir_name, parent_dir = get_absolute_script_path()):
    """Creates a directory in specific parent_dir if the dir_name is not present there.
    dir_name, parent_dir - str."""
    if dir_name not in os_listdir(parent_dir):
        new_path = get_path(parent_dir, dir_name)
        os_mkdir(new_path)

def isdir(folder):
    return os_path_isdir(folder)

def listdir(folder):
    return os_listdir(folder)

class MyDir(object):
    def __init__(self, dir_name, parent_dir = get_absolute_script_path(file = __file__)):
        self.dir_name = dir_name
        self.parent_dir = parent_dir
        self.path = get_path(folder = self.parent_dir, file = self.dir_name)
    def create(self):
        create_dir_if_not_present(dir_name = self.dir_name, parent_dir = self.parent_dir)

