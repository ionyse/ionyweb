# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import PageApp_Sitemap

class PageApp_SitemapForm(ModuloModelForm):

    class Meta:
        model = PageApp_Sitemap