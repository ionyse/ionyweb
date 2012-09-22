# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import Plugin_Image
from ionyweb.file_manager.widgets import FileManagerWidget

class Plugin_ImageForm(ModuloModelForm):

    class Meta:
        model = Plugin_Image
        widgets = {
            'image': FileManagerWidget
        }
        