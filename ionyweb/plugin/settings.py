# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

PLUGIN = {
    'NAME': 'Please configure your PLUGIN_INFO name',
    'SHORT_DESCRIPTION': 'Please configure your PLUGIN_INFO short description',
    'AUTHOR': _(u"Ionyweb Team"),
    'CATEGORY': None,
    'VERSION': "1.0",
    'WEBSITE': None,
    'REQUIREMENTS': None,
    'SCREENSHOT': None,
}

PLUGINS_CATEGORIES = [
    {'slug': 'text','verbose_name': _(u"Text"), 'icon': "admin/css/icons-white/glyphicons_100_font.png"},
    {'slug': 'picture','verbose_name': _(u"Pictures"), 'icon': "admin/css/icons-white/glyphicons_159_picture.png"},
    {'slug': 'audio','verbose_name': _(u"Audio"), 'icon': "admin/css/icons-white/glyphicons_017_music.png"},
    {'slug': 'video','verbose_name': _(u"Video"), 'icon': "admin/css/icons-white/glyphicons_008_film.png"},
    {'slug': 'socialnetwork','verbose_name': _(u"Social network"), 'icon': "admin/css/icons-white/glyphicons_390_facebook.png"},
    {'slug': 'ads','verbose_name': _(u"Advertising"), 'icon': "admin/css/icons-white/glyphicons_227_usd.png"},
    {'slug': 'other','verbose_name': _(u"Other"), 'icon': "admin/css/icons-white/glyphicons_187_more.png"},
]
