# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from ionyweb.widgets import DatePicker
from models import PageApp_Book, Reference

from tinymce.widgets import TinyMCE
from ionyweb.widgets import DatePicker

class PageApp_BookForm(ModuloModelForm):

    class Meta:
        model = PageApp_Book

class ReferenceForm(ModuloModelForm):

    class Meta:
        model = Reference
        exclude = ('book', )
        widgets = {
            'date': DatePicker,
            'description': TinyMCE(attrs={'cols': 80, 'rows': 15,}),
        }

