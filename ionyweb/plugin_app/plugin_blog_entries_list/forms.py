# -*- coding: utf-8 -*-
import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import Plugin_BlogEntriesList, EntryLink


class Plugin_BlogEntriesListForm(ModuloModelForm):

    class Meta:
        model = Plugin_BlogEntriesList
        
#
class EntryLink_Form(ModuloModelForm):
    class Meta:
        model = EntryLink
        exclude = ('plugin', 'order')
