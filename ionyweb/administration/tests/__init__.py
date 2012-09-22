# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from ionyweb.website import create_new_website
from django.test import TransactionTestCase

urls_prefix = u'/%s' % settings.URL_ADMIN_SEP

def test_reverse(*args, **kwargs):
    kwargs['urlconf'] = 'ionyweb.administration.urls'

    return u'%s%s' % (
        urls_prefix,
        reverse(*args, **kwargs)\
            .replace('http://testserver', ''))

class AdministrationTests(TransactionTestCase):
    """Test the extra views djangorestframework provides"""
    urls = 'ionyweb.administration.urls'

    def setUp(self):
        create_new_website(test=True)

from ionyweb.administration.tests.layouts import *
from ionyweb.administration.tests.login import *
from ionyweb.administration.tests.pages import *
from ionyweb.administration.tests.plugins import *
from ionyweb.administration.tests.website import *
from ionyweb.administration.tests.actions import *
from ionyweb.administration.tests.utils import *
