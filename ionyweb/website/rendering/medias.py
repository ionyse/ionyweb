# -*- coding: utf-8 -*-
import os
from django.conf import settings


class AbstractMedia(object):
    """
    Abstract Media object that defines bases of
    medias used in IonyWeb Apps and Plugins.
    """
    def __init__(self, path_file, admin=False, **kwargs):
        self._path_file = path_file
        self._admin = admin

    def get_complete_path_file(self):
        return os.path.join(settings.STATIC_URL,
                            self.prefix_file,
                            self._path_file)

    def _get_class_list(self):
        if self.admin:
            return ['wa_admin',]
        return []

    def _render_class(self):
        class_list = self._get_class_list()
        if class_list:
            return 'class="%s" ' % (' '.join(class_list))
        return ''
        
    @property
    def admin(self):
        return self._admin

    @property
    def prefix_file(self):
        if self.admin:
            return os.path.join('admin', self._prefix_file)
        else:
            return self._prefix_file

    def __eq__(self, other):
        return (self.render() == other.render())

    def __hash__(self):
        return hash(self.render())

    def __unicode__(self):
        return u'<Media : %s> %s' % (
            self.__hash__(), self.render())
        
    def render(self):
        raise NotImplementedError



class AbstractAdminMedia(AbstractMedia):
    """
    Abstract Admin Media object that defines bases
    of medias specific for the IonyWeb Admin.
    """
    def __init__(self, *args, **kwargs):
        # We force the 'admin' parameter
        kwargs['admin'] = True
        super(AbstractAdminMedia, self).__init__(*args, **kwargs)


class RSSMedia(AbstractMedia):
    def __init__(self, *args, **kwargs):
        super(RSSMedia, self).__init__(*args, **kwargs)
        self._title = kwargs.get('title', 'RSS')
        self._rel = 'alternate'
        self._type = 'application/rss+xml'
    
    def render(self):
        return '<link %srel="%s" type="%s" title="%s" href="%s" />' % (
            self._render_class(), self._rel, self._type, self._title,
            self._path_file)
    
class CSSMedia(AbstractMedia):
    """
    CSS Medias for rendering website.
    """
    def __init__(self, *args, **kwargs):
        super(CSSMedia, self).__init__(*args, **kwargs)
        self._prefix_file = kwargs.get('prefix_file', 'css')
        # HTML Attrs
        self._media = kwargs.get('media', 'screen')
        self._type = 'text/css'
        self._rel = 'stylesheet'
        
    def render(self):
        return '<link %srel="%s" type="%s" media="%s" href="%s" />' % (
            self._render_class(), self._rel, self._type, self._media, self.get_complete_path_file())


class JSMedia(AbstractMedia):
    """
    JS Media for rendering website.
    """
    def __init__(self, *args, **kwargs):
        super(JSMedia, self).__init__(*args, **kwargs)
        self._prefix_file = kwargs.get('prefix_file', 'js')
        # HTML Attrs
        self._type = 'text/javascript'
        
    def render(self):
        return '<script %stype="%s" src="%s"></script>' % (
            self._render_class(), self._type, self.get_complete_path_file())


class JSAdminMedia(AbstractAdminMedia, JSMedia):
    """
    JS Medias for IonyWeb Admin.
    """
    pass


class CSSAdminMedia(AbstractAdminMedia, CSSMedia):
    """
    CSS Medias for IonyWeb Admin.
    """
    pass
