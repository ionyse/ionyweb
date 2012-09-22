# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from models import Plugin_Slideshow, Slide


class Plugin_SlideshowForm(ModuloModelForm):
    
    def render_form(self, *args, **kwargs):

        render = super(Plugin_SlideshowForm, self).render_form(*args, **kwargs)
        block_size = render_to_string('plugin_slideshow/current_size_admin.html',
                                      {'object_pk': self.instance.pk,})
        return render+block_size

    class Meta:
        model = Plugin_Slideshow
        exclude =('random',)


class SlideForm(ModuloModelForm):
    class Meta:
        model = Slide
        exclude = ('plugin', 'order')
