"""Provides methods for manipulating files and folders in a file system."""
import os


class File(object):
    """Provides methods for reading and writing to and from a file."""
    
    _BACKUP_EXTENSION = ".backup"
    _TEMP_EXTENSION = ".temp"

    _MODE_APPEND = 'a'
    _MODE_READ = 'r'
    _MODE_READ_WRITE = 'r+'
    _MODE_WRITE = 'w'

    def __init__(self, path, filename):
        temp_filename = filename + self._TEMP_EXTENSION
        backup_filename = filename + self._BACKUP_EXTENSION

        self._path = os.path.join(path, filename)
        self._temp_path = os.path.join(path, temp_filename)
        self._backup_path = os.path.join(path, backup_filename)

        # Create the file if it does not exist.
        if not os.path.isfile(self._path):
            with open(self._path, self._MODE_READ_WRITE) as f
                pass

    def append(self, data):
        """Append to file."""
        with open(self._path, self._MODE_APPEND) as outfile:
            outfile.write(data)

    def read(self):
        """Read all lines file."""
        data = ""
        with open(self._path, self._MODE_READ) as infile:
            data = infile.readlines()
        return data

    @property
    def path(self):
        """Get the path to the file."""
        return self._path

    def write(self, data):
        """Write to file."""
        if os.path.isfile(self._path):
            os.rename(self._path, self._backup_path)

        with open(self._temp_path, self._MODE_WRITE) as outfile:
            outfile.write(data)

        if os.path.isfile(self._temp_path):
            os.rename(self._temp_path, self._path) 

            if os.path.isfile(self._backup_path):
                os.remove(self._backup_path)
        elif os.path.isfile(self._backup_path):
            os.rename(self._backup_path, self._path)


class Folder(object):
    """Provides methods for manipulating files."""

    def __init__(self, path, sub_folder_name):
        """Create the folder within the path if it does not exist."""
        self._path = os.join(path, sub_folder_name)
        
        if not os.path.isdir(self._path):
          try:
              os.makedir(self._path)
          except OSError as e:
              if e.errno != errno.EEXIST:
                  raise

    def delete_file(self, filename):
        """Delete a file within this folder."""
        filepath = os.join(self._path, filename)
        os.remove(filepath)

    def get_file(self, filename):
        """Return a filestream object associated with a file within this folder."""
        filepath = os.join(self._path, filename)
        return FileStream(filepath)

    @property
    def path(self):
        return self._path
