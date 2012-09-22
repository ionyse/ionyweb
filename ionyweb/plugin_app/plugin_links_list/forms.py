# -*- coding: utf-8 -*-

import floppyforms as forms

from ionyweb.forms import ModuloModelForm, ModuloForm
from django.forms.models import modelformset_factory

from models import Plugin_LinksList, Link


class Plugin_LinksListForm(ModuloModelForm):

    class Meta:
        model = Plugin_LinksList



class LinkForm(ModuloModelForm):
    class Meta:
        model = Link
        exclude = ('plugin', 'order')
