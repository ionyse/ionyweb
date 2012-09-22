# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from ionyweb.website.models import WebSite
from ionyweb.page.models import Page
from ionyweb.page_app.page_agenda.models import PageApp_Agenda, Event

from ionyweb.administration.tests import test_reverse, AdministrationTests

class PageAppAgendaTests(AdministrationTests):    
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
        
        page_agenda = PageApp_Agenda.objects.create()

        Page.objects.create(
            website=website, parent=None, title="Home", 
            placeholder_slug="content-placeholder-1",
            plugin_order=0, slug="", 
            app_page_object=page_agenda)
        
        user = User.objects.create_user(username="admin", password="admin")
        user.is_staff = True
        user.save()

        birthday = Event.objects.create(app=page_agenda,
                                        title='My Birthday',
                                        description='Remy\'s birthday',
                                        start_date=datetime.datetime(2012, 2, 21))

    def test_get_pages(self):
        url = '/'
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/p/2012/02/')
        self.assertContains(response, 'Birthday')

        response = self.client.get('/p/2012/02/21/')
        self.assertContains(response, 'Birthday')
        
