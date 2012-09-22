# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from ionyweb.administration.tests import test_reverse, AdministrationTests

from time import time

class WebsiteViewTests(AdministrationTests):

    def test_domains_view(self):
        url = test_reverse('wa-domains')

        # If deconnected, shouldn't work
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # If connected, should work
        self.client.login(username='admin', password='admin')

        response = self.client.get(url)
        self.assertContains(response, 'html')

    def test_domain_get_view(self):
        url = test_reverse('wa-domain')

        # If deconnected, shouldn't work
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # If connected, should work
        self.client.login(username='admin', password='admin')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['edit'], False)

        url = test_reverse('wa-domain', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['edit'], True)

        # If the site doesn't exists
        url = test_reverse('wa-domain', args=[10])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_domain_put_view(self):
        url = test_reverse('wa-domain')
        
        # If connected, should work
        self.client.login(username='admin', password='admin')

        # If the form is empty
        response = self.client.put(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.context['edit'], False)

        # If the domain aready exists
        response = self.client.put(url, {'domain': 'testserver'})
        self.assertEqual(response.status_code, 400)

        # If it is a subdomain of a RESTRICTED_DOMAIN
        saved_restricted_domains = settings.RESTRICTED_DOMAINS
        settings.RESTRICTED_DOMAINS = ['bar.com']
        response = self.client.put(url, {'domain': 'foo.bar.com'})
        self.assertEqual(response.status_code, 400)

        # If everything is ok
        response = self.client.put(url, {'domain': 'foobar.com'})
        self.assertContains(response, 'msg')

        settings.RESTRICTED_DOMAINS = saved_restricted_domains

    def test_domain_post_view(self):
        url = test_reverse('wa-domain', args=[1])
        
        # If connected, should work
        self.client.login(username='admin', password='admin')

        # If the form is empty
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

        # If the site doesn't exists
        url = test_reverse('wa-domain', args=[10])
        response = self.client.post(url, {'domain': 'mydomainname.com'})
        self.assertEqual(response.status_code, 404)

        # We create a new site
        put_url = test_reverse('wa-domain')
        response = self.client.put(put_url, {'domain': 'mydomainname.com'})
        self.assertContains(response, 'msg')

        pk = Site.objects.get(domain='mydomainname.com').pk
        # If the domain already exists shouldn't work
        url = test_reverse('wa-domain', args=[pk])
        response = self.client.post(url, {'domain': 'testserver'})
        self.assertEqual(response.status_code, 400)

        # If nothing changed
        url = test_reverse('wa-domain', args=[pk])
        response = self.client.post(url, {'domain': 'mydomainname.com'})
        self.assertEqual(response.status_code, 200)

        # If the change was ok
        url = test_reverse('wa-domain', args=[pk])
        response = self.client.post(url, {'domain': 'example.com'})
        self.assertEqual(response.status_code, 200)

    def test_domain_delete_view(self):
        # If connected, should work
        self.client.login(username='admin', password='admin')

        # We create a new site
        put_url = test_reverse('wa-domain')
        self.client.put(put_url, {'domain': 'mydomainname.com'})

        pk = Site.objects.get(domain='mydomainname.com').pk        

        # If everything ok
        url = test_reverse('wa-domain', args=[pk])
        response = self.client.delete(url)
        self.assertContains(response, 'msg')
        
        # If the site doesn't exists
        url = test_reverse('wa-domain', args=[10])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        
        # If the site is the primary site
        url = test_reverse('wa-domain', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)
