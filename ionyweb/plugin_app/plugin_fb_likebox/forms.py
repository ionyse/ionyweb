# -*- coding: utf-8 -*-
import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import Plugin_FbLikebox


class Plugin_FbLikeboxForm(ModuloModelForm):

    class Meta:
        model = Plugin_FbLikebox