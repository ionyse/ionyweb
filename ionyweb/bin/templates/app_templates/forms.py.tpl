# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import PageApp_{{ app_object_name }}

class PageApp_{{ app_object_name }}Form(ModuloModelForm):

    class Meta:
        model = PageApp_{{ app_object_name }}
