# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from models import *

admin.site.register(PageApp_Agenda)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_description_admin', 'start_date', 'is_published', 'last_modif', 'app')
    date_hierarchy = 'start_date'
    list_filter = ('app', 'is_published')
    ordering = ['-start_date']
    fieldsets = (
                     (_(u'Arborescence'), { 'fields': ('app', 'is_published',) }),
                     (_(u'Quand ?'), { 'fields':  ('start_date', 'end_date') }),
                     (_(u'Quoi ?'), { 'fields': ('title', 'description', 'image') }),
                     (_(u'Où ?'), { 'fields': ('place', 'address', 'zipcode', 'city') }),
                     )
    search_fields = ['description',]


admin.site.register(Event, EventAdmin)
