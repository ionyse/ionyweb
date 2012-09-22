# -*- coding: utf-8 -*-

from datetime import datetime
import floppyforms as forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from ionyweb.forms import ModuloModelForm
from ionyweb.widgets import DatePicker
from models import Entry, Category, PageApp_Blog

from ionyweb.widgets import DateTimePicker, SlugWidget, DatePicker, TinyMCELargeTable


class PageApp_BlogForm(ModuloModelForm):

    class Meta:
        model = PageApp_Blog


class CategoryForm(ModuloModelForm):

    class Meta:
        model = Category
        exclude = ('blog', )
        widgets = {
            'slug': SlugWidget('name'),
        }

class EntryForm(ModuloModelForm):
    author = forms.ModelChoiceField(label=_('author'),
                                    queryset=User.objects.all(), 
                                    empty_label=None)

    def __init__(self, authors_choices, categories_set, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = categories_set
        self.fields['author'].choices = authors_choices

    class Meta:
        model = Entry
        exclude = ('blog', )
        widgets = {
            'publication_date': DateTimePicker,
            'body': TinyMCELargeTable(attrs={'cols': 80, 'rows': 15,}),
            'slug': SlugWidget('title'),
        }
