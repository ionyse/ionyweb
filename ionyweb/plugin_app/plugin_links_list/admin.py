# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class LinksListAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'nb_links')

class LinkAdmin(admin.ModelAdmin):
    list_display = ('text', 'target', 'plugin', 'order')
    list_filter = ('plugin',)
    ordering = ('text',)
    
admin.site.register(Plugin_LinksList, LinksListAdmin)
admin.site.register(Link, LinkAdmin)
