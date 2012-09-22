# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from models import *
from forms import ReferenceForm


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'date', 'description')
    list_display_links = ('title',)
    list_filter = ['client', 'categories']
    ordering = ['-date']
    search_fields = ['title', 'client__name']

    use_fieldsets = (
        ('Arborescence', {
            'fields': ('section','client')}),
        (None, {
            'fields': ('title',
                       'description',
                       'date',
                       'img',
                       'url',
                       'categories')
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']

admin.site.register(PageApp_Book)
admin.site.register(Client)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Category, CategoryAdmin)
