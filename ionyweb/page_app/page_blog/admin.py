# -*- coding: utf-8 -*-
"""
Administration interface options of ``blog`` application.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ionyweb.page_app.page_blog.models import PageApp_Blog, Category, Entry

class CategoryAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Category`` model.
    """
    list_display = ('name', 'slug', 'creation_date', 'modification_date')
    search_fields = ('name',)
    date_hierarchy = 'creation_date'
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}

class EntryAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``Entry`` model.
    """
    list_display = ('title', 'category', 'status', 'author')
    search_fields = ('title', 'body')
    date_hierarchy = 'publication_date'
    fieldsets = (
        (_('Headline'), {'fields': ('blog', 'author', 'title', 'slug', 'category')}),
        (_('Publication'), {'fields': ('publication_date', 'status')}),
        (_('Body'), {'fields': ('body',)}),
    )
    save_on_top = True
    radio_fields = {'status': admin.VERTICAL}
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(PageApp_Blog)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
