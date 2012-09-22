# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from ionyweb.administration.tests import test_reverse, AdministrationTests

class ActionsViewTests(AdministrationTests):
        
    def test_dispatcher_view(self):
        "Test the access point actions in API - Dispatcher Views"

        valid_html_id_plugin = '%s%d' % (settings.HTML_ID_PLUGIN, 1)
        valid_html_id_app = '%s%d' % (settings.HTML_ID_APP, 1)
        valid_url_action = 'item_list'

        url = test_reverse('wa-actions', args=[valid_html_id_plugin,
                                               valid_url_action])

        # If deconnected, shouldn't work
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 403)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        
        # Connection of client
        self.client.login(username='admin', password='admin')
        
        # Call with bad number of parameters
        self.assertRaises(NoReverseMatch, test_reverse, 'wa-actions')
        self.assertRaises(NoReverseMatch, test_reverse,
                          'wa-actions', args=[valid_html_id_plugin])
        self.assertRaises(NoReverseMatch, test_reverse,
                          'wa-actions', args=[valid_url_action])

        # Call with wrong object_slug
        # Wrong prefix
        wrong_html_id_plugin = 'wrong-slug-1'
        url = test_reverse('wa-actions', args=[wrong_html_id_plugin,
                                               valid_url_action])
        response = self.client.get(url)
        self.assertContains(response, 'msg', status_code=400)
        response = self.client.put(url)
        self.assertContains(response, 'msg', status_code=400)
        response = self.client.post(url)
        self.assertContains(response, 'msg', status_code=400)
        response = self.client.delete(url)
        self.assertContains(response, 'msg', status_code=400)

        # Plugin Relation Object doesn't exist
        html_id_plugin = '%s%d' % (settings.HTML_ID_PLUGIN, 10000)
        url = test_reverse('wa-actions', args=[html_id_plugin,
                                               valid_url_action])
        response = self.client.get(url)
        self.assertContains(response, 'msg', status_code=404)
        response = self.client.put(url)
        self.assertContains(response, 'msg', status_code=404)
        response = self.client.post(url)
        self.assertContains(response, 'msg', status_code=404)
        response = self.client.delete(url)
        self.assertContains(response, 'msg', status_code=404)

        # App Object doesn't exist
        html_id_app = '%s%d' % (settings.HTML_ID_APP, 100000)
        url = test_reverse('wa-actions', args=[html_id_app,
                                               valid_url_action])
        response = self.client.get(url)
        self.assertContains(response, 'msg', status_code=404)

        # If HTML ID is OK and object exists,
        # must return the plugin/app action
        # corresponding to the url action param.
        
        # TODO for plugin object and app object
