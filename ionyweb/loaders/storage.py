import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.utils.importlib import import_module
from django.utils._os import safe_join
from django.contrib.staticfiles import utils

from ionyweb import get_ionyweb_path


class LayoutStorage(FileSystemStorage):
    """
    Layout storage
    """
    prefix = 'layouts'

    def __init__(self, location=None, *args, **kwargs):
        if location is None:
            sys.stderr.write('\n\n'+str(location)+'\n\n')
            location = os.path.join(get_ionyweb_path(), 'contrib', 'layouts')

        super(LayoutStorage, self).__init__(location, *args, **kwargs)

    def listdir(self, path):
        path = self.path(path)
        directories, files = [], []
        for entry in os.listdir(path):
            if entry != 'layout.html':
                if os.path.isdir(os.path.join(path, entry)):
                    directories.append(entry)
                else:
                    files.append(entry)
        return directories, files

class ThemeStorage(FileSystemStorage):
    """
    Themes storage
    """

    prefix = 'themes'

    def __init__(self, location=None, *args, **kwargs):
        if location is None:
            sys.stderr.write('\n\n'+str(location)+'\n\n')
            location = os.path.join(get_ionyweb_path(), 'contrib', 'themes')
        
        super(ThemeStorage, self).__init__(location, *args, **kwargs)

    def listdir(self, path):
        
        path = self.path(path)
        directories, files = [], []
        for entry in os.listdir(path):
            
            if entry != 'templates':
                if os.path.isdir(os.path.join(path, entry)):
                    directories.append(entry)
                else:
                    files.append(entry)
        return directories, files
