# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

PLUGIN_INFO = {
    'NAME': _(u"{{ plugin_name }}"),
    'CATEGORY': 'text',
    'VERSION': "1.0",
    'SHORT_DESCRIPTION': _(u"Please edit plugin_{{ plugin_name|lower }}./__init__.py"),
    'DESCRIPTION': _(u"Please edit plugin_{{ plugin_name|lower }}./__init__.py"),
}
