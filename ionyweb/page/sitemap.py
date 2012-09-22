# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap
from ionyweb.page.models import Page

class PagesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Page.objects.filter(draft=False)

    def lastmod(self, obj):
        return obj.last_modif
