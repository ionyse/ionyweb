# -*- coding: utf-8 -*-

import floppyforms as forms
import datetime
from django.conf import settings

from tinymce.widgets import TinyMCE

class DatePicker(forms.TextInput):
    template_name = 'floppyforms/date.html'
    format="%d/%m/%Y"

    def render(self, name, value, attrs=None):
            if isinstance(value, datetime.date):
                    value=value.strftime(self.format)

            return super(DatePicker, self).render(name, value, attrs)

    class Media:
        css = {
            'all': ('actions_admin/css/dark-hive/styles.css',)
        }

#

class DateTimePicker(forms.TextInput):
    template_name = 'floppyforms/datetime.html'
    format="%d/%m/%Y %H:%M"

    def render(self, name, value, attrs=None):
            if isinstance(value, datetime.datetime):
                value=value.strftime(self.format)
            return super(DateTimePicker, self).render(name, value, attrs)

    class Media:
        css = {
            'all': ('actions_admin/css/dark-hive/styles.css',)
        }

#

class SlugWidget(forms.widgets.SlugInput):
    template_name = 'floppyforms/slug.html'

    
    def __init__(self, prepopulated_from, attrs=None):
        self.prepopulated_from = prepopulated_from
        super(SlugWidget, self).__init__(attrs)

    def get_context_data(self):
        context = super(SlugWidget, self).get_context_data()
        context['field_id'] = 'id_%s' % self.prepopulated_from
        return context

    class Media:
        js = (settings.ADMIN_MEDIA_PREFIX+'js/urlify.js',)
        


class TinyMCELargeTable(TinyMCE):

    def render(self, name, value, attrs=None):
        return u'</td></tr><tr><td colspan="2">%s' \
            %super(TinyMCELargeTable, self).render(name, value, attrs)

class TinyMCESimple(TinyMCE):
    def __init__(self, content_language=None, attrs=None, mce_attrs=None):
        compiled_attrs = {'style': 'width: 430px; height: 100px'}
        if attrs is not None:
            compiled_attrs.update(attrs)
        super(TinyMCE, self).__init__(compiled_attrs)
        if mce_attrs is None:
            mce_attrs = {'theme': 'simple'}
        self.mce_attrs = mce_attrs
        if content_language is None:
            content_language = mce_attrs.get('language', None)
        self.content_language = content_language

class Slider(forms.RangeInput):
    min = 1
    max = 18
    step = 1
    template_name = 'floppyforms/slider.html'

    class Media:
        css = {
            'all': (
                'actions_admin/css/dark-hive/styles.css',
            )
        }


class TemplateThemeSelectWidget(forms.widgets.RadioSelect):
    template_name = 'floppyforms/template_theme_select.html'
