"""Provides methods for manipulating files and folders in a file system."""


class File(object):

    def __init__(self, path, filename):
        pass

    def append(self, data):
        pass

    def read(self):
        pass

    @property
    def path(self):
        pass

    def write(self, data):
        pass


class Folder(object):

    def __init__(self, path, sub_folder_name):
        pass

    def delete_file(self, filename):
        pass

    def get_file(self, filename):
        pass

    @property
    def path(self):
        pass
