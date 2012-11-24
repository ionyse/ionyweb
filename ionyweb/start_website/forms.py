# -*- coding: utf-8 -*-
from django.conf import settings
import floppyforms as forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

class StartWebsite(forms.Form):
    name = forms.CharField(label=_(u'Name'), max_length=50, initial=settings.SITE_NAME)
    slug = forms.CharField(label=_(u'Slug'), max_length=50, initial=slugify(settings.SITE_NAME))
    domain = forms.CharField(label=_(u'Domain'), max_length=100, initial='localhost:8000')

    theme = forms.CharField(label=_(u'Theme slug'), 
                            max_length=100, 
                            initial='notmyidea')

    layout = forms.CharField(label=_(u'Default layout'), 
                             max_length=100, 
                             initial='100',
                             widget=forms.HiddenInput)
