# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from django.contrib.contenttypes.models import ContentType
from ionyweb.plugin.settings import PLUGIN, PLUGINS_CATEGORIES
import importlib


# First, get list of users
plugins = ContentType.objects.filter(model__startswith='plugin_').order_by('name')
list_plugin = [{'name': p.model_class(),
                'id': p.id}
               for p in plugins]

PLUGINS_LIST = {}
for category in PLUGINS_CATEGORIES:
    PLUGINS_LIST[category['slug']] = []

for i in list_plugin:
    
    plugin_info = PLUGIN.copy()
    # Dynamic call to from ionyweb.plugin_app.plugin_contact import PLUGIN_INFO
    info = importlib.import_module(i['name'].__module__.rsplit('.',1)[0]).PLUGIN_INFO

    plugin_info.update(info)

    if info.get('CATEGORY') != None and info['CATEGORY'] in PLUGINS_LIST:
            PLUGINS_LIST[info['CATEGORY']].append({'name':info['NAME'], 'description': info['SHORT_DESCRIPTION'], 'id': i['id']})
    else:
        PLUGINS_LIST['other'].append({'name':info['NAME'], 'description': info['SHORT_DESCRIPTION'], 'id': i['id']})


#PLUGINS_LIST = sorted(list_plugin, key=lambda x: x['name'])
