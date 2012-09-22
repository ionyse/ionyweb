# -*- coding: utf-8 -*-
from django.conf import settings
from ionyweb.administration.tests import test_reverse, AdministrationTests
from django.contrib.contenttypes.models import ContentType
from ionyweb.page.models import Page


class PageViewTests(AdministrationTests):
    def test_pages_view(self):
        url = test_reverse('wa-pages')

        # If deconnected, shouldn't work
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin', password='admin')

        # GET - list of pages
        response = self.client.get(url)
        self.assertContains(response, 'page_list')
        self.assertEqual(len(response.context['pages']), 91)

    def test_page_layout_view(self):
        url = test_reverse('wa-page-layout')

        # If deconnected, shouldn't work
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin', password='admin')

        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url, {'layout_section_slug': settings.SLUG_CONTENT})
        self.assertContains(response, settings.SLUG_CONTENT)

    def test_get_page_view(self):
        url = test_reverse('wa-page')

        # If deconnected, shouldn't work
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='admin', password='admin')

        # GET - new page form
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # GET - Add a child
        response = self.client.get(url, {'parent': 1})
        self.assertContains(response, '<input type=\\"hidden\\" name=\\"parent\\" value=\\"1\\"')

        # GET - edit form
        url = test_reverse('wa-page', args=[1])
        response = self.client.get(url)
        self.assertContains(response, '<input id=\\"id_title\\" type=\\"text\\" name=\\"title\\" value=\\"Home\\" maxlength=\\"255\\" />')
        # Homepage doesn't show slug field
        self.assertContains(response, '<input type=\\"hidden\\" name=\\"slug\\" id=\\"id_slug\\">')
        # Other form page displays the slug field
        url = test_reverse('wa-page', args=[2])
        response = self.client.get(url)
        self.assertContains(response, '<input type=\\"text\\" name=\\"slug\\" value=\\"section_1\\"')


    def test_put_page_view(self):
        self.client.login(username='admin', password='admin')
        url = test_reverse('wa-page')

        app_page_type = ContentType.objects.get(
            app_label="page_text", model="pageapp_text").id

        ## Try to create a child for the home page
        infos = {'title': 'New page',
                 'slug': 'new-page',
                 'parent': 1,
                 'app_page_type': app_page_type}
        response = self.client.put(url, infos)
        self.assertEqual(response.status_code, 400)

        ## Try to create an empty slug page
        infos = {'title': 'New page',
                 'slug': '',
                 'parent': '',
                 'app_page_type': app_page_type}
        response = self.client.put(url, infos)
        self.assertEqual(response.status_code, 400)

        ## Try to create a used slug page
        infos = {'title': 'New page',
                 'slug': 'section_1',
                 'parent': '',
                 'app_page_type': app_page_type}
        response = self.client.put(url, infos)
        self.assertEqual(response.status_code, 400)

        ## Too short slug
        infos = {'title': 'New page',
                 'slug': 'p',
                 'parent': '',
                 'app_page_type': app_page_type}
        response = self.client.put(url, infos)
        self.assertEqual(response.status_code, 400)

        ## Parent doesn't exists
        infos = {'title': 'New page',
                 'slug': 'new-page',
                 'parent': 9999,
                 'app_page_type': app_page_type}
        response = self.client.put(url, infos)
        self.assertEqual(response.status_code, 400)

        ## Working add form
        infos = {'title': 'New page',
                 'slug': 'new-page',
                 'parent': '',
                 'app_page_type': app_page_type}
        response = self.client.put(url, infos)
        self.assertEqual(response.status_code, 202)

        ## Working add child form
        infos = {'title': 'New page 2',
                 'slug': 'new-page2',
                 'parent': 10,
                 'app_page_type': app_page_type}
        response = self.client.put(url, infos)
        self.assertEqual(response.status_code, 202)

    def test_page_move_previous(self):
        self.client.login(username='admin', password='admin')
        url = test_reverse('wa-page', args=[10])
        response = self.client.post(url, {'move': '',
                                          'previous': 8,})
        self.assertEqual(response.status_code, 200)

    def test_page_move_next(self):
        self.client.login(username='admin', password='admin')
        url = test_reverse('wa-page', args=[10])
        response = self.client.post(url, {'move': '',
                                          'next': 12,})
        self.assertEqual(response.status_code, 200)

    def test_page_move_parent(self):
        self.client.login(username='admin', password='admin')

        # Move another page
        url = test_reverse('wa-page', args=[10])
        response = self.client.post(url, {'move': '',
                                          'parent': 11,})
        self.assertEqual(response.status_code, 200)

        # Refresh when current page url changed
        page_20 = Page.objects.get(pk=20).get_absolute_url()
        url = page_20[:-1] + test_reverse('wa-page', args=[20])
        response = self.client.post(url, {'move': '',
                                          'parent': 15,})
        self.assertEqual(response.status_code, 202)

        # Refresh when parent page url changed
        page_24 = Page.objects.get(pk=24).get_absolute_url()
        url = page_24[:-1] + test_reverse('wa-page', args=[22])
        response = self.client.post(url, {'move': '',
                                          'parent': 14})
        self.assertEqual(response.status_code, 202)
        
    def test_page_toggle_draft(self):
        self.client.login(username='admin', password='admin')
        url = test_reverse('wa-page', args=[10])
        response = self.client.post(url, {'draft': '', })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Page.objects.get(pk=10).draft, True)

        url = test_reverse('wa-page', args=[10])
        response = self.client.post(url, {'draft': '', })
        self.assertEqual(Page.objects.get(pk=10).draft, False)
        
    def test_post_page_view(self):
        self.client.login(username='admin', password='admin')
        url = test_reverse('wa-page', args=[10])

        app_page_type = ContentType.objects.get(
            app_label="page_text", model="pageapp_text").id

        # Post the form to modify the page
        url = test_reverse('wa-page', args=[22])
        response = self.client.post(url, {'title': 'New page 2',
                                          'slug': 'section_3',
                                          'parent': 10,
                                          'app_page_type': app_page_type})
        self.assertEqual(response.status_code, 200)

        # Slug is too short
        response = self.client.post(url, {'title': 'New page 2',
                                          'slug': 'p',
                                          'parent': 10,
                                          'app_page_type': app_page_type})
        self.assertEqual(response.status_code, 203)

        # Try to change the Homepage Slug
        url = test_reverse('wa-page', args=[1])
        response = self.client.post(url, {'title': 'HomePage',
                                          'slug': 'homepage',
                                          'parent': None,
                                          'app_page_type': app_page_type})
        self.assertEqual(response.status_code, 203)

        # Try to set en empty slug to a page
        page_23 = Page.objects.get(pk=23)
        url = test_reverse('wa-page', args=[page_23.pk])
        response = self.client.post(url, {'title': page_23.title,
                                          'slug': '',
                                          'parent': page_23.parent.id,
                                          'app_page_type': page_23.app_page_type.id})
        self.assertEqual(response.status_code, 203)


    def test_delete_page_view(self):
        self.client.login(username='admin', password='admin')

        # Try to delete the home page (And failed)
        url = test_reverse('wa-page', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

        # When we delete the current page, redirect
        page_20 = Page.objects.get(pk=20).get_absolute_url()
        url = page_20[:-1] + test_reverse('wa-page', args=[20])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 202)
        
        # When trying to delete a normal page
        url = test_reverse('wa-page', args=[10])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

