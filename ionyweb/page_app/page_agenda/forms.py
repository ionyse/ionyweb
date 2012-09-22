# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import PageApp_Agenda, Event
from ionyweb.file_manager.widgets import FileManagerWidget
from ionyweb.widgets import TinyMCESimple, DateTimePicker

class PageApp_AgendaForm(ModuloModelForm):
    class Meta:
        model = PageApp_Agenda

class EventForm(ModuloModelForm):
    class Meta:
        model = Event
        exclude = ('app',)
        widgets = {
            'image': FileManagerWidget,
            'description': TinyMCESimple,
            'start_date': DateTimePicker,
            'end_date': DateTimePicker
            }
