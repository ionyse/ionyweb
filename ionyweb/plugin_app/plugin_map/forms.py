# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.widgets import Slider
from ionyweb.forms import ModuloModelForm
from models import Plugin_Map

from django.conf import settings
from django.template.loader import render_to_string

class DoNotDisplay(forms.TextInput):
    template_name = 'floppyforms/donotdisplay.html'

class Plugin_MapForm(ModuloModelForm):

    def render_form(self):
        form = render_to_string('plugin_maps/form.html',
                                {'map': self.instance,
                                 'form': self,
                                 'STATIC_URL': settings.STATIC_URL})
	return form

    class Meta:
        model = Plugin_Map
        widgets = {
            'address': DoNotDisplay,
            'map_lat': forms.HiddenInput,
            'map_lon': forms.HiddenInput
        }

    class Media:
        js = ('js/plugin_map.js',)
