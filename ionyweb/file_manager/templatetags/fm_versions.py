# coding: utf-8

# PYTHON IMPORTS
import os, re
from time import gmtime

# DJANGO IMPORTS
from django.template import Library, Node, Variable, VariableDoesNotExist, TemplateSyntaxError
from django.conf import settings
from django.utils.encoding import force_unicode, smart_str
from django.core.files import File

from ionyweb.settings import VERSIONS
from ionyweb.file_manager.functions import storage, get_version_path, version_generator

register = Library()


class VersionNode(Node):
    
    def __init__(self, src, version_prefix):
        self.src = Variable(src)
        
        if (version_prefix[0] == version_prefix[-1] and version_prefix[0] in ('"', "'")):
            self.version_prefix = version_prefix[1:-1]
        else:
            self.version_prefix = None
            self.version_prefix_var = Variable(version_prefix)
        
    def render(self, context):
        try:
            source = self.src.resolve(context)
        except VariableDoesNotExist:
            return None

        if self.version_prefix:
            version_prefix = self.version_prefix
        else:
            try:
                version_prefix = self.version_prefix_var.resolve(context)
            except VariableDoesNotExist:
                return None
        
        website = context.get('website', None)
        
        if website is None:
            request = context.get('request', None)
            website = getattr(request, 'website')
        
        directory = website.media_root()
        if directory is None:
            return ""
        
        try:
            if isinstance(source, File):
                source = source.name
            source = force_unicode(source)
            if source.startswith(settings.MEDIA_URL):
                source = source[len(settings.MEDIA_URL):]
            version_path = get_version_path(source, version_prefix, directory)
            
            if not storage.exists(version_path):
                version_path = version_generator(source, version_prefix, directory)
            elif storage.modified_time(source) > storage.modified_time(version_path):
                version_path = version_generator(source, version_prefix, directory, force=True)
            return storage.url(version_path)
        except:
            raise
            return ""


def version(parser, token):
    """
    Displaying a version of an existing Image according to the predefined VERSIONS settings.
    {% version field_name.path version_prefix %}
    
    Use {% version my_image.path 'medium' %} in order to display the medium-size
    version of an Image stored in a field name my_image.
    
    version_prefix can be a string or a variable. if version_prefix is a string, use quotes.
    """
    
    try:
        tag, src, version_prefix = token.split_contents()
    except:
        raise TemplateSyntaxError, "%s tag requires 2 arguments" % token.contents.split()[0]
    
    if (version_prefix[0] == version_prefix[-1] and version_prefix[0] in ('"', "'")) and version_prefix.lower()[1:-1] not in VERSIONS:
        raise TemplateSyntaxError, "%s tag received bad version_prefix %s" % (tag, version_prefix)
    return VersionNode(src, version_prefix)


register.tag(version)
