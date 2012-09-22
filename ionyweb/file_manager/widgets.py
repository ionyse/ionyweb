# coding: utf-8

import floppyforms as forms
from django.conf import settings

class FileManagerWidget(forms.TextInput):
    template_name = 'floppyforms/filemanager.html'

    def get_context(self, *args, **kwargs):
        ctx = super(FileManagerWidget, self).get_context(*args, **kwargs)
        ctx['STATIC_URL'] = settings.STATIC_URL
        return ctx