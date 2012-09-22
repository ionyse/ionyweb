# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import Plugin_WebsiteTitle


class Plugin_WebsiteTitleForm(ModuloModelForm):

    class Meta:
        model = Plugin_WebsiteTitle
