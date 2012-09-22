# -*- coding: utf-8 -*-
" Context Processor of the Aeris project "

import warnings

from django.conf import settings
from django.utils.translation import ugettext as _

from ionyweb.page.models import Page


def user_rights(request):
    return {'is_admin': request.is_admin,
            'is_superuser': request.is_superuser}

def admin_page_data(request):
    if request.is_admin and hasattr(request, 'page'):
        return {"page": request.page}
    else:
        return {}


def site_settings(request):
    return {
        'DOMAIN_DNS_CNAME': getattr(settings, 
                                    'DOMAIN_DNS_CNAME',
                                    settings.DOMAIN_NAME),
        'CROSSDOMAIN_AUTH_URL': getattr(settings,
                                        'CROSSDOMAIN_AUTH_URL',
                                        None)
        }
