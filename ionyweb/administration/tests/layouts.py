# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.administration.tests import test_reverse, AdministrationTests

class LayoutViewTests(AdministrationTests):
    def test_layouts_view(self):
        """Ensure the layouts view exists"""
        url = test_reverse('wa-layouts')

        # If deconnected, shouldn't work
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # If connected, should work
        self.client.login(username='admin', password='admin')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        
        response = self.client.get(url, {'layout_section_slug': settings.SLUG_CONTENT})
        self.assertContains(response, 'layouts_listform')
        
    def test_layout_view(self):
        # Test the preview
        url = test_reverse('wa-layout')
        
        self.client.login(username='admin', password='admin')

        # No parameters
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        # Preview content
        response = self.client.get(url, {'layout_section_slug': settings.SLUG_CONTENT})
        self.assertContains(response, settings.SLUG_CONTENT)

        # Preview other layouts
        response = self.client.get(url, {'layout_section_slug': 'foobar'})
        self.assertContains(response, 'foobar')
        
        # No parameters
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

        # Edit
        response = self.client.post(url, {'layout_section_slug': settings.SLUG_CONTENT, 
                                          'layout_template_slug': '100_50_50_100'})
        self.assertContains(response, 'msg')
