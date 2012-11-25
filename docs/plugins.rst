==========================
Creating your first plugin
==========================

You have some app defined in the ionyweb code:

 - plugin_contact
 - plugin_map
 - plugin_website_title
 - plugin_fb_likebox
 - plugin_slideshow
 - plugin_blog_entries_list
 - plugin_image
 - plugin_text
 - plugin_breadcrumb
 - plugin_links_list
 - plugin_video

You can use this plugins as an example or directly in your project.


Create the plugin skeleton
==========================

::

    $ cd YOUR_PROJECT
    $ ionyweb-manage startplugin YOUR_PLUGIN_NAME
    Starting creation of : inscription
    
    Plugin dir created.
    Plugin Models file created.
    Plugin Views created.
    Plugin Forms created.
    Plugin Admin created.
    Plugin Templates created.
    Locale dir created.
    
    
    Now just define your models,
    Custom the default template : 'index.html',
    Add your plugin to your INSTALLED_APPS : 'plugin_YOUR_PLUGIN_NAME'
    Synchronise the database.
     => Your plugin is fully configured !
    
    $ python manage.py schemamigration plugin_YOUR_PLUGIN_NAME --initial
	$ python manage.py migrate plugin_YOUR_PLUGIN_NAME


You can now create your plugin.


Configure the plugin
====================

As an example, we will create an inscription plugin that will take the
name and email address of a guest and save it in the database.


Create the plugin model
=======================

Let's edit the ``plugin_inscription/models.py`` file::

    # -*- coding: utf-8 -*-
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from ionyweb.plugin.models import AbstractPlugin
    
    
    class Plugin_Inscription(AbstractPlugin):
        
        # Define your fields here
    
        def __unicode__(self):
            return u'Inscription #%d' % (self.pk)
    
        class Meta:
            verbose_name = _(u"Inscription")


    class Guest(models.Model):
        name = models.CharField(_('name'), max_length=100)
        email = models.EmailField(_('email'))

        def __unicode__(self):
            return u'%s' % self.name


Edit the plugin manifest
========================

Since a plugin is a python package, we can edit its plugin_info in the ``__init__.py`` file::

    # -*- coding: utf-8 -*-
    from django.utils.translation import ugettext as _
    
    PLUGIN_INFO = {
        'NAME': _(u"Inscription"),
        'CATEGORY': 'socialnetwork',
        'VERSION': "1.0",
        'SHORT_DESCRIPTION': _(u"Inscription form."),
        'DESCRIPTION': _(u"Guest inscription form."),
    }

You can choice category in the list:

 - text
 - picture
 - audio
 - video
 - socialnetwork
 - ads
 - other

By default, it will be other.


Add your plugin
===============

A plugin always has a title that you can decide to hide.

By default the template is ``plugin_inscription/templates/plugin_inscription/index.html``::

    <p>That the plugin Inscription</p>


Create the inscription form
---------------------------

Let's defined our form ``plugin_inscription/forms.py``::

    # -*- coding: utf-8 -*-
    import floppyforms as forms
    from ionyweb.forms import ModuloModelForm
    from models import Plugin_Inscription, Guest
    
    
    class Plugin_InscriptionForm(ModuloModelForm):
    
        class Meta:
            model = Plugin_Inscription


    class Guest(ModuloModelForm):
        class Meta:
            model = Guest


Load the form in the view
-------------------------

We modify a little bit the default view, to manage the form::
    
    # -*- coding: utf-8 -*-
    from django.template import RequestContext
    from django.utils.translation import ugettext_lazy as _
    from ionyweb.website.rendering.utils import render_view
    from forms import GuestForm
    
    # from ionyweb.website.rendering.medias import CSSMedia, JSMedia, JSAdminMedia
    MEDIAS = (
        # App CSS
        # CSSMedia('plugin_inscription.css'),
        # App JS
        # JSMedia('plugin_inscription.js'),
        # Actions JSAdmin
        # JSAdminMedia('plugin_inscription_actions.js'),
        )
    
    def index_view(request, plugin):
        form = GuestForm()
        message = None
    
        if request.method == "POST" and not request.is_admin_url:
            # Check if we submit this specific form.
            if int(request.POST['inscription_form']) == plugin.pk:
                form = GuestForm(request.POST)
                if form.is_valid():
                    form.save()
                    message = _(u'Inscription saved')
                    form = GuestForm()
                else:
                    message = _(u'There is some errors in your form.')
    
        return render_view('plugin_inscription/index.html',
                           {'object': plugin,
                            'form': form,
                            'message': message},
                           MEDIAS,
                           context_instance=RequestContext(request))

We create the template::

    {% load i18n %}    
    <div class="iw-plugin-inscription">
    
      {% include 'themes/plugin_app_title.html' %}
    
      {% if message %}
      <div class="alert {% if form.errors %}alert-error{% else %}alert-success{% endif %}">
    	{{ message }}
      </div>
      {% endif %}
    
      <form action="" method="post">
        {{ form.as_p }}
    	<input type="hidden" name="inscription_form" value="{{ object.pk }}" />
    	<div><button type="submit" class="btn">{% trans "Save" %}</button></div>
      </form>
    
    </div>


Create the administration
=========================

We will create the administration to be able to see our inscription
list.

First create the ``wa_actions_urls.py`` file::

    # -*- coding: utf-8 -*-
    from django.conf.urls import patterns, url
    
    from ionyweb.administration.actions.utils import get_actions_urls
    
    from models import Guest
    from forms import GuestForm
    
    # Generic Action View
    urlpatterns = get_actions_urls(Guest,
                                   form_class=GuestForm)

Then create the ``static/admin/js/plugin_inscription_actions.js`` file::

    admin.plugin_inscription = {
        edit_guests : function(relation_id){
    		admin.GET({
    			url : '/wa/action/' + relation_id + '/guest_list/',
    		});
        },
    }

Then add the action to the ``Plugin_Inscription`` class::

    class Plugin_Inscription(AbstractPlugin):
        
        # Define your fields here
    
        def __unicode__(self):
            return u'Inscription #%d' % (self.pk)
    
        class Meta:
            verbose_name = _(u"Inscription")
    
        class ActionsAdmin:
            actions_list = (
                {'title':_(u'Edit guests'),
                 'callback': "admin.plugin_inscription.edit_guests"},
                )

Also load the ``JSAdminFile`` with the view::

    from ionyweb.website.rendering.medias import JSAdminMedia
    MEDIAS = (
        # Actions JSAdmin
        JSAdminMedia('plugin_inscription_actions.js'),
        )
