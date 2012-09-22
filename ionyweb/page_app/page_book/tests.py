# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

urls_prefix = u'/references/%s' % settings.URL_PAGE_APP_SEP

def test_reverse(*args, **kwargs):
    kwargs['urlconf'] = 'philanthropix.page_book.urls'

    return u'%s%s' % (
        urls_prefix,
        reverse(*args, **kwargs)\
            .replace('http://testserver', ''))

class BookTest(TestCase):
    """
    Tests of ``book`` application.
    """
    fixtures = ['test_data.yaml']

    def test_book_index(self):
        """
        Tests ``book_archive`` view.

        """
        url = '%s/' % '/'.join(urls_prefix.split('/')[:-1]) # '/book/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
