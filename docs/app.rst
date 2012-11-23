=======================
Creating your first app
=======================

You have some app defined in the ionyweb code:

 - page_blog
 - page_redirect
 - page_text
 - page_agenda
 - page_book
 - page_gallery_images
 - page_sitemap

You can use this apps as an example or directly in your project.


Create the app skeleton
=======================

::

    $ cd YOUR_PROJECT
    $ ionyweb-manage startapp YOUR_APP_NAME
    Starting creation of : YOUR_APP_NAME
    
    App dir created.
    App Models file created.
    App Views created.
    App Forms created.
    App Urls created.
    App Admin created.
    App Templates created.
    App Locale dir created.
    
    
    Now just define your models,
    Custom the default template : 'index.html',
    Add your app to your INSTALLED_APPS : 'page_YOUR_APP_NAME'
    Synchronise the database.
     => Your app is fully configured !
    $ python manage.py syncdb
    Syncing...
    Creating tables ...
    Creating table page_YOUR_APP_NAME_pageapp_YOUR_APP_NAME
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)

You can now create page of your new type. But it is as empty as possible.


Configure the app
=================

Let's say we want to create a list of music groups.

We will need this kind of data:

 - Country with country code
 - Music style
 - Group informations

Country and Music gender are not related to the page but we want to be
able to create different list of group for each pages.


Create the app models
+++++++++++++++++++++

If we open the generated ``page_group/models.py`` file we have::

    # -*- coding: utf-8 -*-
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from ionyweb.page.models import AbstractPageApp
    
    
    class PageApp_Group(AbstractPageApp):
        
        # Define your fields here
    
        def __unicode__(self):
            return u'Group #%d' % (self.pk)
    
        class Meta:
            verbose_name = _(u"Group")
    
This is the minimum to define a Ionyweb Page App.

We will add some other models::

    class Country(models.Model):
        """A list of countries."""
        code = models.CharField(_(u'code'), max_length=2, primary_key=True, 
                                help_text=_(u"See <a href='http://nephi.unice.fr/"
                                            u"codes_iso_pays.php' target='_blank'>"
                                            u"the country code list</a>."))
    
        name = models.CharField(_(u'name'), max_length=75)
    
        def __unicode__(self):
            return u'%s' % self.name
    
        class Meta:
            verbose_name = _(u'Country')
            verbose_name_plural = _(u"Countries")
    
    
    class MusicStyle(models.Model):
        """A list of music type."""
        name = models.CharField(_(u'name'), max_length=30, unique=True)
    
        def __unicode__(self):
            return u'%s' % self.name
    
    
    class Group(models.Model):
        app = models.ForeignKey(PageApp_Group, related_name="groups")
    
        music_style = models.ForeignKey(MusicStyle, related_name="groups")
        countries = models.ManyToManyField(Country, related_name="groups")
    
        code = models.CharField(_(u'code'), max_length=5, help_text=_(u"Exemple C002 ou MA201"))
        photo =  models.CharField(_("photo"), max_length=200, blank=True)
    
        name = models.CharField(_(u'name'), max_length=100)
        description = models.TextField(_(u'description'), blank=True)
    
        class Meta:
            ordering = ('code',)
    
        def __unicode__(self):
            return u"%s : %s" % (self.code, self.name)
    
        def class_css(self):
            style_class = re.search('^[a-zA-Z]+', self.code)
            return style_class.group(0)


Create the app view
+++++++++++++++++++

Next we want to display the group list on our page.

If we open the generated ``page_group/views.py`` file we have::

    # -*- coding: utf-8 -*-
    
    from django.template import RequestContext
    from ionyweb.website.rendering.utils import render_view
    
    # from ionyweb.website.rendering.medias import CSSMedia, JSMedia, JSAdminMedia
    MEDIAS = (
        # App CSS
        # CSSMedia('page_group.css'),
        # App JS
        # JSMedia('page_group.js'),
        # Actions JSAdmin
        # JSAdminMedia('page_group_actions.js'),
        )
    
    def index_view(request, page_app):
        return render_view('page_group/index.html',
                           { 'object': page_app, },
                           MEDIAS,
                           context_instance=RequestContext(request))


You can provide some medias specific to your app views and to your app
administration.

The index view is the default. It is defined in the urls.py::

    # -*- coding: utf-8 -*-
    
    from django.conf.urls import patterns, url
    from views import index_view
    
    urlpatterns = patterns('',
                           url(r'^$', index_view),
                           )

Lets modify the template  ``page_group/templates/page_group/index.html`` file we have::

    <p>That the app Group.</p>

We will change it for::

    <h1>My list of groups</h1>
    <ul>
        {% for group in object.groups.all %}
        <li>{{ group }}</li>
        {% empty %}
        <li>No groups yet</li>
        {% endfor %}
    </ul>


Creating the administration
+++++++++++++++++++++++++++

We need to create a page_group/wa_actions_urls.py file::

    # -*- coding: utf-8 -*-
    from ionyweb.administration.actions.utils import get_actions_urls
    
    from models import Country, MusicStyle, Group
    
    urlpatterns = get_actions_urls(Country)
    urlpatterns += get_actions_urls(MusicStyle)
    urlpatterns += get_actions_urls(Group)
