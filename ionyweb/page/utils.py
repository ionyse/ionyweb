# -*- coding: utf-8 -*-
import floppyforms as forms

from django import forms as django_forms
from django.conf import settings


def errors_append(form, field_name, message):
    u'''
    Add an ValidationError to a field (instead of __all__) during Form.clean():

    class MyForm(forms.Form):
        def clean(self):
            value_a=self.cleaned_data['value_a']
            value_b=self.cleaned_data['value_b']
            if value_a==... and value_b==...:
                formutils.errors_append(self, 'value_a', u'Value A must be ... if value B is ...')
            return self.cleaned_data
    '''
    assert form.fields.has_key(field_name), field_name
    error_list=form.errors.get(field_name)
    if error_list is None:
        error_list = django_forms.util.ErrorList()
        form.errors[field_name] = error_list
    error_list.append(message)
