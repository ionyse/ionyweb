# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.administration.tests import test_reverse, AdministrationTests
from django.contrib.contenttypes.models import ContentType

class PluginViewTests(AdministrationTests):
    def test_plugins_view(self):
        url = test_reverse('wa-plugins')

        # If deconnected, shouldn't work
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        self.assertContains(response, 'plugins_listform')

    def test_get_plugin_pk_view(self):
        self.client.login(username='admin', password='admin')

        # Try to edit an existing plugin of the page
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 3)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.get(url)
        self.assertContains(response, 'html')

        # Try to edit an existing plugin of another page
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 16)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.get(url)
        self.assertContains(response, 'html')

        # Try to edit a non existing plugin
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 9999)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # Try to edit another website plugin
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 487)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        

    def test_get_plugin_view(self):
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')

        # Some fields are missing
        response = self.client.get(url)
        self.assertContains(response, 'msg', status_code = 400)

        response = self.client.get(url, {'placeholder_id': ''})
        self.assertContains(response, 'msg', status_code = 400)

        response = self.client.get(url, {'plugin_type': ''})
        self.assertContains(response, 'msg', status_code = 400)

        # Fields are Ok
        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        plugin_id = ContentType.objects.get(
            app_label="plugin_text", model="plugin_text").id

        # Everything ok - Should work
        response = self.client.get(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'plugin_form_form', status_code = 200)

        # Wrong placeholder
        response = self.client.get(url, {'placeholder_id': 'foobar',
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'msg', status_code = 400)

        # Cannot add in placeholder_default
        response = self.client.get(url, {'placeholder_id': settings.HTML_ID_PLACEHOLDER_DEFAULT,
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'msg', status_code = 400)

        # Cannot add in placeholder clipboard
        response = self.client.get(url, {'placeholder_id': settings.HTML_ID_PLACEHOLDER_CLIPBOARD,
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'msg', status_code = 400)

        # Wrong plugin_id
        response = self.client.get(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': 9999})
        self.assertContains(response, 'msg', status_code = 400)

        
    def test_put_plugin_view(self):
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')
        
        # Some fields are missing
        response = self.client.put(url)
        self.assertContains(response, 'msg', status_code = 400)

        response = self.client.put(url, {'placeholder_id': ''})
        self.assertContains(response, 'msg', status_code = 400)

        response = self.client.put(url, {'plugin_type': ''})
        self.assertContains(response, 'msg', status_code = 400)

        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        plugin_id = ContentType.objects.get(
            app_label="plugin_text", model="plugin_text").id

        # Wrong placeholder
        response = self.client.put(url, {'placeholder_id': 'foobar',
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'msg', status_code = 400)

        # Cannot add in placeholder_default
        response = self.client.put(url, {'placeholder_id': settings.HTML_ID_PLACEHOLDER_DEFAULT,
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'msg', status_code = 400)

        # Cannot add in placeholder clipboard
        response = self.client.put(url, {'placeholder_id': settings.HTML_ID_PLACEHOLDER_CLIPBOARD,
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'msg', status_code = 400)

        # Wrong plugin_id
        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': 9999})
        self.assertContains(response, 'msg', status_code = 400)

        # Empty form
        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'plugin_form_form', status_code = 400)

        # Form ok
        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id,
                                         'text': '<p>Foo bar</p>'})
        self.assertContains(response, 'msg')
        self.assertContains(response, 'html')

    def test_post_plugin_view(self):
        self.client.login(username='admin', password='admin')

        # OK - Try to edit an existing plugin of the page
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 3)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.post(url, {'text': '<p>Another value</p>'})
        self.assertContains(response, 'html')
        self.assertContains(response, 'msg')

        # OK - Try to edit an existing plugin of another page
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 16)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.post(url, {'text': '<p>Another value</p>'})
        self.assertContains(response, 'html')
        self.assertContains(response, 'msg')

        # 404 - Try to edit a non existing plugin
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 9999)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.post(url, {'text': '<p>Another value</p>'})
        self.assertEqual(response.status_code, 404)

        # 404 - Try to edit another website plugin
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 487)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.post(url, {'text': '<p>Another value</p>'})
        self.assertEqual(response.status_code, 404)

        # 400 - Empty form
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 3)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.post(url, {})
        self.assertContains(response, 'plugin_form_form', status_code = 400)


    def test_delete_plugin_view(self):
        self.client.login(username='admin', password='admin')

        # OK - Try to edit an existing plugin of the page
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 3)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.delete(url)
        self.assertContains(response, 'msg')

        # OK - Try to edit an existing plugin of another page
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 16)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.delete(url)
        self.assertContains(response, 'msg')

        # 404 - Try to edit a non existing plugin
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 9999)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

        # 404 - Try to edit another website plugin
        arg = '%s%d' % (settings.HTML_ID_PLUGIN, 487)
        url = test_reverse('wa-plugin', args=[arg])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_plugin_page_relation_view(self):
        self.client.login(username='admin', password='admin')

        url = test_reverse('wa-plugin-page-relation')

        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        content_placeholder_2 = '%s2' % settings.HTML_ID_PLACEHOLDER_CONTENT
        clipboard_placeholder = '%s' % settings.HTML_ID_PLACEHOLDER_CLIPBOARD
        default_placeholder = '%s' % settings.HTML_ID_PLACEHOLDER_DEFAULT
        plugins_order = ['plugin-relation-2', 
                         'plugin-relation-1']
        app = '%s1' % settings.HTML_ID_APP

        # 400 - Some fields are missing
        response = self.client.post(url)
        self.assertContains(response, 'msg', status_code = 400)

        response = self.client.post(url, {'placeholder_id': content_placeholder_1})
        self.assertContains(response, 'msg', status_code = 400)

        response = self.client.post(url, {'plugins_order[]': plugins_order})
        self.assertContains(response, 'msg', status_code = 400)

        # 400 - Wrong placeholder
        response = self.client.post(url, {'placeholder_id': 'foobar',
                                         'plugins_order[]': plugins_order})
        self.assertContains(response, 'msg', status_code = 400)

        # Ok - Try to move and reorder some plugins
        response = self.client.post(url, {'placeholder_id': content_placeholder_1,
                                         'plugins_order[]': plugins_order})
        self.assertContains(response, 'msg')

        # OK - Try to move the page_app
        response = self.client.post(url, {'placeholder_id': content_placeholder_2,
                                          'plugins_order[]': [app]})
        self.assertContains(response, 'msg')

        # 400 - Try to move another website plugin
        response = self.client.post(url, {'placeholder_id': content_placeholder_1,
                                          'plugins_order': ['plugin-relation-2', 
                                                            'plugin-relation-487']})
        self.assertContains(response, 'msg', status_code = 400)

        # Ok - Try to move another page plugin
        response = self.client.post(url, {'placeholder_id': content_placeholder_1,
                                          'plugins_order[]': ['plugin-relation-2', 
                                                            'plugin-relation-16']})
        self.assertContains(response, 'msg')

        # Ok - Try to move the plugin in the clipboard
        response = self.client.post(url, {'placeholder_id': clipboard_placeholder,
                                          'plugins_order[]': ['plugin-relation-2']})
        self.assertContains(response, 'msg')

        # Fail - Try to move the app in the clipboard
        response = self.client.post(url, {'placeholder_id': clipboard_placeholder,
                                          'plugins_order[]': [app]})
        self.assertContains(response, 'msg', status_code = 400)

        # Fail - Try to move something in the default
        response = self.client.post(url, {'placeholder_id': default_placeholder,
                                          'plugins_order[]': plugins_order})
        self.assertContains(response, 'msg', status_code = 400)
