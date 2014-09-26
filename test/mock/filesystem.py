"""Provides mock objects for powl.filesystem."""


class MockFile(object):

    @property
    def read_retval(self):
        return self._read_retval

    @read_retval.setter
    def read_retval(self, value):
        self._read_retval = value

    @property
    def append_data(self):
        return self._append_data

    @append_data.setter
    def append_data(self, value):
        self._append_data = value

    @property
    def append_line_data(self):
        return self._append_line_data

    @append_line_data.setter
    def append_line_data(self, value):
        self._append_line_data = value

    # powl.filesystem.File methods
    def __init__(self, path, filename):
        self._path = path
        self._filename = filename
        self._read_retval = ""
        self._append_data = ""
        self._append_line_data = ""
        self._write_data = ""

    def append(self, data):
        self._append_data = value

    def append_line(self, data):
        self._append_line_data = value

    def empty(self):
        return False

    @property
    def filename(self):
        return self._filename

    def read(self):
        return self._read_retval

    @property
    def path(self):
        return self._path

    def write(self, data):
        self._write_data = data


class NullFolder(object):

    def __init__(self, path, sub_folder_name):
        pass

    def delete_file(self, filename):
        pass

    def get_file(self, filename):
        pass

    @property
    def path(self):
        pass
