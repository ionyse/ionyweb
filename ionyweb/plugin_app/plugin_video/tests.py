# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from ionyweb.website.models import WebSite
from ionyweb.page.models import Page
from ionyweb.page_app.page_text.models import PageApp_Text
from django.contrib.contenttypes.models import ContentType

from ionyweb.administration.tests import test_reverse, AdministrationTests

class PluginVideoTests(AdministrationTests):    
    def setUp(self):
        # Create website with a IonywebSubscription home page
        # Create the domain name
        site = Site.objects.get_or_create(pk=1)[0]
        site.domain = "testserver"
        site.name = "Jungleland"
        site.save()
    
        # Create the website
        website = WebSite.objects.create(
            title="Jungleland", theme="jungleland",
            default_layout="100", slug="jungleland", 
            domain=site)
        website.ndds.add(site)
        
        page_text = PageApp_Text.objects.create(text="Bienvenue")

        Page.objects.create(
            website=website, parent=None, title="Home", 
            placeholder_slug="content-placeholder-1",
            plugin_order=0, slug="", 
            app_page_object=page_text)
        
        user = User.objects.create_user(username="admin", password="admin")
        user.is_staff = True
        user.save()        

    def test_get_video_form(self):
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')

        # Fields are Ok
        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        plugin_id = ContentType.objects.get(
            app_label="plugin_video", model="plugin_video").id

        # Everything ok - Should work
        response = self.client.get(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id})
        self.assertContains(response, 'plugin_form_form', status_code = 200)

    def test_youtube_video(self):
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')
        
        # Create the youtube video
        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        plugin_id = ContentType.objects.get(
            app_label="plugin_video", model="plugin_video").id

        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id,
                                         'url': 'http://www.youtube.com/watch?v=n7vYo6l06lo'})
        self.assertContains(response, 'msg')

        # Display the youtube video
        self.client.logout()
        url = '/'

        response = self.client.get(url)
        self.assertContains(response, 'n7vYo6l06lo')

        # Shorten URL
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')
        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id,
                                         'url': 'http://youtu.be/n7vYo6l06lo'})
        self.assertContains(response, 'msg')
        
    
    def test_dailymotion_video(self):
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')
        
        # Create the dailymotion video
        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        plugin_id = ContentType.objects.get(
            app_label="plugin_video", model="plugin_video").id

        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id,
                                         'url': 'http://www.dailymotion.com/video/xogb25_il-s-evanouit-quand-on-le-chatouille_news'})
        self.assertContains(response, 'msg')

        # Display the dailymotion video
        self.client.logout()
        url = '/'

        response = self.client.get(url)
        self.assertContains(response, 'xogb25')

        # Shorten URL
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')
        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id,
                                         'url': 'http://dai.ly/zIc0si'})
        self.assertContains(response, 'msg')


    def test_vimeo_video(self):
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')
        
        # Create the vimeo video
        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        plugin_id = ContentType.objects.get(
            app_label="plugin_video", model="plugin_video").id

        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id,
                                         'url': 'http://vimeo.com/35256030'})
        self.assertContains(response, 'msg')

        # Display the vimeo video
        self.client.logout()
        url = '/'

        response = self.client.get(url)
        self.assertContains(response, '35256030')

    def test_facebook_video(self):
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')
        
        # Create the facebook video
        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        plugin_id = ContentType.objects.get(
            app_label="plugin_video", model="plugin_video").id

        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id,
                                         'url': 'https://www.facebook.com/video/video.php?v=1498994573921'})
        self.assertContains(response, 'msg')

        response = self.client.put(url, {'placeholder_id': content_placeholder_1,
                                         'plugin_type': plugin_id,
                                         'url': 'https://www.facebook.com/photo.php?v=1498994573921'})
        self.assertContains(response, 'msg')

        # Display the facebook video
        self.client.logout()
        url = '/'

        response = self.client.get(url)
        self.assertContains(response, '1498994573921')


    def test_unknown_video(self):
        url = test_reverse('wa-plugin')
        self.client.login(username='admin', password='admin')
        
        # Try to create a NotImplemented Video
        content_placeholder_1 = '%s1' % settings.HTML_ID_PLACEHOLDER_CONTENT
        plugin_id = ContentType.objects.get(
            app_label="plugin_video", model="plugin_video").id

        response = self.client.put(url, {
                'placeholder_id': content_placeholder_1,
                'plugin_type': plugin_id,
                'url': 'http://www.wat.tv/video/depression-potes-bande-annonce-4yvwp_2ffyh_.html'})
        self.assertContains(response, 'msg', status_code = 400)
