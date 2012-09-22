# -*- coding: utf-8 -*-
import floppyforms as forms
from django.template.loader import render_to_string


class ModuloForm:
    def render_form(self):
        return self.as_table()


class ModuloModelForm(forms.ModelForm, ModuloForm):
    pass

class IonywebContentForm(object):

    def __init__(self, *args, **kwargs):
        self.inline_help_text = kwargs.pop('inline_help_text', False)
        super(IonywebContentForm, self).__init__(*args, **kwargs)

    def render_basic_form(self):
        return render_to_string('forms/content_basic_form.html',
                                {'form': self})
