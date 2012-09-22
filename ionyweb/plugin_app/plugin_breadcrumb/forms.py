# -*- coding: utf-8 -*-
import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import Plugin_Breadcrumb


class Plugin_BreadcrumbForm(ModuloModelForm):

    class Meta:
        model = Plugin_Breadcrumb