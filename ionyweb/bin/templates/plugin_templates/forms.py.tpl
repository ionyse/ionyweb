# -*- coding: utf-8 -*-
import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import Plugin_{{ plugin_object_name }}


class Plugin_{{ plugin_object_name }}Form(ModuloModelForm):

    class Meta:
        model = Plugin_{{ plugin_object_name }}
