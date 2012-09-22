# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import PageApp_Redirect

class PageApp_RedirectForm(ModuloModelForm):

    class Meta:
        model = PageApp_Redirect
        widgets = {
            'url': forms.URLInput,
        }
