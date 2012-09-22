# -*- coding: utf-8 -*-
from django import template

from ionyweb.plugin_app.plugin_slideshow.models import FX_VALUES

register = template.Library()


@register.filter(name='slideshow_fx')
def slideshow_fx(value):
    for code, verbose_name, value_fx in FX_VALUES:
        if code == value:
            return value_fx
    return 'fade'
