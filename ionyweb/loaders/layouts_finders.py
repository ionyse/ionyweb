import os
from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder
from django.utils.datastructures import SortedDict
from django.utils.importlib import import_module
from django.utils._os import safe_join
from django.contrib.staticfiles import utils

from ionyweb.loaders.storage import LayoutStorage

class StaticFinder(BaseFinder):

    def __init__(self, apps=None, *args, **kwargs):
        self.locations = list(getattr(settings, 'LAYOUTS_DIRS', []))

        # Maps dir paths to an appropriate storage instance
        self.storages = SortedDict()

        for root in self.locations:
            filesystem_storage = LayoutStorage(location=root)
            self.storages[root] = filesystem_storage

        super(StaticFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the theme locations
        as defined in ``LAYOUTS_DIRS``.
        """
        matches = []
        for root in self.locations:
            matched_path = self.find_location(root, path)
            if matched_path:
                if not all:
                    return matched_path
                matches.append(matched_path)
        return matches

    def find_location(self, root, path):
        """
        Finds a requested static file in a location, returning the found
        absolute path (or ``None`` if no match).
        """
        dirs = path.split('/')
        if len(dirs) >= 3 and dirs[0] == 'layouts':
            path = u'/'.join(dirs[1:])
            if path.find('layout.html') != -1:
                return None
            else:
                path = safe_join(root, path)
                if os.path.exists(path):
                    return path
        else:
            return None

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for root in self.locations:
            storage = self.storages[root]
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage
