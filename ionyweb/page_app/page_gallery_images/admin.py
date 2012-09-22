# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class ImageAdmin(admin.ModelAdmin):
    
    list_filter = ['album']


admin.site.register(PageApp_GalleryImages)
admin.site.register(Album)
admin.site.register(Image, ImageAdmin)
