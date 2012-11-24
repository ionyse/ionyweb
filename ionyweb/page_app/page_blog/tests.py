# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from ionyweb.website.models import WebSite
from ionyweb.page_app.page_blog.models import PageApp_Blog, Category, Entry
from ionyweb.page.models import Page

import datetime

urls_prefix = u'/blog/%s' % settings.URL_PAGE_APP_SEP

def test_reverse(*args, **kwargs):
    kwargs['urlconf'] = 'ionyweb.page_app.page_blog.urls'

    return u'%s%s' % (
        urls_prefix,
        reverse(*args, **kwargs)\
            .replace('http://testserver', ''))

class BlogTest(TestCase):
    """
    Tests of ``blog`` application.
    """
    def setUp(self):
        # Create website with a IonywebSubscription home page
        # Create the domain name
        site = Site.objects.get_or_create(pk=1)[0]
        site.domain = "testserver"
        site.name = "Jungleland"
        site.save()

        me = User.objects.create_user('admin', 'admin@ionyse.com', 'admin')

        # Create the website
        website = WebSite.objects.create(
            title="Jungleland", theme="notmyidea",
            default_layout="100", slug="jungleland", 
            domain=site)
        website.ndds.add(site)
        
        page_blog = PageApp_Blog.objects.create(title="Foo bar")

        page_home = Page.objects.create(
            website=website, parent=None, title="Blog", 
            placeholder_slug="content-placeholder-1",
            plugin_order=0, slug="blog", 
            app_page_object=page_blog)

        category_offline = Category.objects.create(name="Offline", slug="offline", parent=None, blog=page_blog)
        category_test = Category.objects.create(name="Test", slug="test", parent=None, blog=page_blog)

        entry_test = Entry.objects.create(blog=page_blog, author=me, title="Test Entry", slug="test-entry", body="<p>foo bar</p>", publication_date=datetime.date(2010, 07, 21), status=1, category=category_test)
        entry_offline = Entry.objects.create(blog=page_blog, author=me, title="Offline", slug="offline", body="<p>foo bar</p>", publication_date=datetime.date(2010, 07, 21), status=0, category=category_offline)


    def test_entry_archive_index(self):
        """
        Tests ``entry_archive`` view.

        """
        url = '%s/' % '/'.join(urls_prefix.split('/')[:-1]) # '/blog/'
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)

    def test_entry_archive_year(self):
        """
        Tests ``entry_archive_year`` view.
        """
        url = test_reverse('blog_year', args=['2010'])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)

    def test_entry_archive_month(self):
        """
        Tests ``entry_archive_month``view.
        """
        url = test_reverse('blog_month', args=['2010', '07'])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)

    def test_entry_archive_day(self):
        """
        Tests ``entry_archive_day`` view.
        """
        url = test_reverse('blog_day', args=['2010', '07', '21'])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)

    def test_entry_detail(self):
        """
        Tests ``entry_detail`` view.
        """
        url = test_reverse('blog_entry', args=['2010', '07', '21', 'test-entry'])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)

    def test_entry_detail_not_found(self):
        """
        Test ``entry_detail`` view with an offline entry.
        """
        url = test_reverse('blog_entry', args=['2010', '07', '21', 'offline-entry'])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 404)

    def test_category_detail(self):
        """
        Tests ``category_detail`` view.
        """
        url = test_reverse('blog_category', args=['test'])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)

    def test_category_detail_not_found(self):
        """
        Tests ``category_detail`` view with an offline category.
        """
        url = test_reverse('blog_category', args=['offline'])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 404)

    def test_rss_entries(self):
        """
        Tests entries RSS feed.
        """
        url = test_reverse('blog_rss_entries_feed')
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        
    def test_rss_category(self):
        """
        Tests categories RSS feed.
        """
        from ionyweb.page_app.page_blog.models import Category
        categories = Category.online_objects.all()
        for category in categories:
            url = test_reverse('blog_rss_category_feed', args=[category.slug])
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, 200)
