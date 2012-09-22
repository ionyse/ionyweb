# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.conf import settings
from django.utils.translation import ugettext as _

from ionyweb.loaders.manifest import list_themes, themes_info

def get_list_design(request):
    """
        Return a list of all design available
        
        [{slug: 'design1', data:{author: 'ionyse', 'thumbnail': '', ...}},
         {slug: 'design1', data:{author: 'ionyse', 'thumbnail': '', ...}}, etc ...]
    """
    return themes_info()

def get_themes_for_design(request, design=None):
    """
        Return a list of all theme available for a design with a specific slug (arg design)
    """
    if not design:
        return None
    return ""
    