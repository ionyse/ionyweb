"""
Wrapper for loading templates from "themes" directories in ionyweb.
"""

import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.utils._os import safe_join
from django.utils.importlib import import_module


# At compile time, cache the directories to search.
app_template_dirs = list(getattr(settings, 'THEMES_DIRS', []))

# It won't change, so convert it to a tuple to save memory.
app_template_dirs = tuple(app_template_dirs)

class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        
        if not template_dirs:
            template_dirs = app_template_dirs
        
        
        dirs = template_name.split('/')
        if len(dirs) >= 3 and dirs[0] == 'themes':
            template_name = u'/'.join([dirs[1], dirs[2], 'templates']+dirs[3:])
            
            
        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, template_name)
            except UnicodeDecodeError:
                # The template dir name was a bytestring that wasn't valid UTF-8.
                raise
            except ValueError:
                # The joined path was located outside of template_dir.
                pass
        

    def load_template_source(self, template_name, template_dirs=None):
        
        
        for filepath in self.get_template_sources(template_name, template_dirs):
            try:
                file = open(filepath)
                try:
                    return (file.read().decode(settings.FILE_CHARSET), filepath)
                finally:
                    file.close()
            except IOError:
                pass
        raise TemplateDoesNotExist(template_name)

_loader = Loader()

def load_template_source(template_name, template_dirs=None):
    # For backwards compatibility
    import warnings
    warnings.warn(
        "'ionyweb.layout.template_loader.load_template_source' is deprecated; use 'ionyweb.layout.template_loader.Loader' instead.",
        DeprecationWarning
    )
    return _loader.load_template_source(template_name, template_dirs)
load_template_source.is_usable = True
