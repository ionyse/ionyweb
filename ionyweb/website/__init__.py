# -*- coding: utf-8 -*-

import sys

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from django.db import connection

from ionyweb.website.models import WebSite, WebSiteOwner
from ionyweb.page.models import Page, Layout
from ionyweb.page_app.page_text.models import PageApp_Text
from ionyweb.plugin_app.plugin_website_title.models import Plugin_WebsiteTitle
from ionyweb.plugin_app.plugin_text.models import Plugin_Text
from ionyweb.plugin.models import PluginRelation

def flush_website(interactive=True):

    # flush the database
    if interactive:
        confirm = raw_input("""You have requested a flush of the database.
This will IRREVERSIBLY DESTROY all data currently in the %r database,
and return each table to the state it was in after syncdb.
Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: """ % connection.settings_dict['NAME'])
    else:
        confirm = 'yes'

    if confirm == 'yes':
        cursor = connection.cursor()
        query = 'DROP DATABASE `%s`;\n' % connection.settings_dict['NAME']
        sys.stderr.write(query)
        try:
            cursor.execute(query)
        except:
            pass

        query = 'CREATE DATABASE `%s` CHARACTER SET utf8 COLLATE utf8_general_ci;\n' % connection.settings_dict['NAME']
        sys.stderr.write(query)
        cursor.execute(query)
    

def create_new_website(test=False):
    """ This create a empty brand new website with the minimum and
    correct content-type
    """

    # Create the domain name
    site = Site.objects.get_or_create(pk=1)[0]
    site.domain = test and "testserver" or "localhost:8000"
    site.name = "Jungleland"
    site.save()

    # Create the website
    website = WebSite.objects.create(
        title="Jungleland", theme="jungleland",
        default_layout="100", slug="jungleland", 
        domain=site)
    website.ndds.add(site)

    # Create the admin user
    user = User.objects.create_user(
        'admin', 'contact@ionyse.com', 'admin')
    user.is_staff = True
    user.save()

    # The user own the website
    wo = WebSiteOwner.objects.create(
        website=website, user=user, is_superuser=True)

    # Create a Home Page
    page_text = PageApp_Text.objects.create(
        text='<p>Bienvenue sur Jungleland</p>')

    page_home = Page.objects.create(
        website=website, parent=None, title="Home", 
        placeholder_slug="content-placeholder-1",
        plugin_order=0, slug="", 
        app_page_object=page_text)

    pt = Plugin_Text.objects.create(text='Text 1')
    pr = PluginRelation.objects.create(content_object=pt,
                                       placeholder_slug='content-placeholder-2',
                                       plugin_order=0)
    pr.pages.add(page_home)

    pt = Plugin_Text.objects.create(text='Text 2')
    pr = PluginRelation.objects.create(content_object=pt,
                                       placeholder_slug='content-placeholder-3',
                                       plugin_order=0)
    pr.pages.add(page_home)

    pt = Plugin_Text.objects.create(text='Text 3')
    pr = PluginRelation.objects.create(content_object=pt,
                                       placeholder_slug='content-placeholder-4',
                                       plugin_order=0)
    pr.pages.add(page_home)

    layout = Layout.objects.create(slug = 'content', 
                                   template = "100_33-33-33_100",
                                   related_object = page_home)

    for page in xrange(1,10):
        page_text = PageApp_Text.objects.create(
            text='<p>Bienvenue sur la section %s</p>' % page)

        current_page = Page.objects.create(
            website=website, parent=None, title="Section %s" % page, 
            placeholder_slug="content-placeholder-1",
            plugin_order=0, slug="section_%s" % page, 
            app_page_object=page_text)

        for plugin in xrange(1,5):
            pt = Plugin_Text.objects.create(text='Text %s-%s' % (page, plugin))
            pr = PluginRelation.objects.create(content_object=pt,
                                               placeholder_slug='content-placeholder-%s' % plugin,
                                               plugin_order=0)
            pr.pages.add(current_page)
            
        for sub_page in xrange(1,10):
            page_text = PageApp_Text.objects.create(
                text='<p>Bienvenue sur la section %s.%s</p>' % (page, sub_page))

            child_page = Page.objects.create(
                website=website, parent=current_page, title="Section %s.%s" % (page, sub_page), 
                placeholder_slug="content-placeholder-1",
                plugin_order=0, slug="section_%s_%s" % (page, sub_page), 
                app_page_object=page_text)

            for plugin in xrange(1,5):
                pt = Plugin_Text.objects.create(text='Text %s-%s-%s' % (page, sub_page, plugin))
                pr = PluginRelation.objects.create(content_object=pt,
                                                   placeholder_slug='content-placeholder-%s' % plugin,
                                                   plugin_order=0)
                pr.pages.add(child_page)


    layout = Layout.objects.create(slug = 'content', 
                                   template = "100_25-25-25-25_100",
                                   related_object = website)
    ### CREATE A SECOND WEBSITE
    # Create the domain name
    site = Site.objects.create(domain='foobar.com:8000', name='Second Website')

    # Create the website
    website = WebSite.objects.create(
        title="Second Website", theme="jungleland",
        default_layout="100", slug="foobar", 
        domain=site)
    website.ndds.add(site)

    # The user own the website
    wo = WebSiteOwner.objects.create(
        website=website, user=user, is_superuser=True)

    # Create a Home Page
    page_text = PageApp_Text.objects.create(
        text='<p>Bienvenue sur Second Website</p>')

    page_home = Page.objects.create(
        website=website, parent=None, title="Home", 
        placeholder_slug="content-placeholder-1",
        plugin_order=0, slug="", 
        app_page_object=page_text)

    pt = Plugin_Text.objects.create(text='Text 1')
    pr = PluginRelation.objects.create(content_object=pt,
                                       placeholder_slug='content-placeholder-2',
                                       plugin_order=0)
    pr.pages.add(page_home)

    pt = Plugin_Text.objects.create(text='Text 2')
    pr = PluginRelation.objects.create(content_object=pt,
                                       placeholder_slug='content-placeholder-3',
                                       plugin_order=0)
    pr.pages.add(page_home)

    pt = Plugin_Text.objects.create(text='Text 3')
    pr = PluginRelation.objects.create(content_object=pt,
                                       placeholder_slug='content-placeholder-4',
                                       plugin_order=0)
    pr.pages.add(page_home)

    layout = Layout.objects.create(slug = 'content', 
                                   template = "100_33-33-33_100",
                                   related_object = page_home)

    for page in xrange(1,10):
        page_text = PageApp_Text.objects.create(
            text='<p>Bienvenue sur la section %s</p>' % page)

        current_page = Page.objects.create(
            website=website, parent=None, title="Section %s" % page, 
            placeholder_slug="content-placeholder-1",
            plugin_order=0, slug="section_%s" % page, 
            app_page_object=page_text)

        for plugin in xrange(1,5):
            pt = Plugin_Text.objects.create(text='Text %s-%s' % (page, plugin))
            pr = PluginRelation.objects.create(content_object=pt,
                                               placeholder_slug='content-placeholder-%s' % plugin,
                                               plugin_order=0)
            pr.pages.add(current_page)
            
        for sub_page in xrange(1,10):
            page_text = PageApp_Text.objects.create(
                text='<p>Bienvenue sur la section %s.%s</p>' % (page, sub_page))

            child_page = Page.objects.create(
                website=website, parent=current_page, title="Section %s.%s" % (page, sub_page), 
                placeholder_slug="content-placeholder-1",
                plugin_order=0, slug="section_%s_%s" % (page, sub_page), 
                app_page_object=page_text)

            for plugin in xrange(1,5):
                pt = Plugin_Text.objects.create(text='Text %s-%s-%s' % (page, sub_page, plugin))
                pr = PluginRelation.objects.create(content_object=pt,
                                                   placeholder_slug='content-placeholder-%s' % plugin,
                                                   plugin_order=0)
                pr.pages.add(child_page)


    layout = Layout.objects.create(slug = 'content', 
                                   template = "100_25-25-25-25_100",
                                   related_object = website)
