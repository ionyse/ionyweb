# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import Plugin_Text

from ionyweb.widgets import TinyMCELargeTable

class Plugin_TextForm(ModuloModelForm):

    class Meta:
        model = Plugin_Text
        
        widgets = {
            'text': TinyMCELargeTable(attrs={'style': 'width: 100%; height: 300px;', }),
        }
