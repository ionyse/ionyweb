# -*- coding: utf-8 -*-
" Page engine models "

import os.path
from hashlib import sha1

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve
from django.conf import settings
from django.template.loader import get_template

from mptt.models import MPTTModel

from ionyweb.website.models import WebSite
from ionyweb.page.exceptions import PageAppAdminNotProperlyConfiguredError

from copy import copy, deepcopy

from django.db.models.deletion import Collector
from django.db.models.fields.related import ForeignKey


class Page(MPTTModel):
    """Page of a website
    """    
    # -- Hierarchy pages infos

    website = models.ForeignKey(WebSite,
                                related_name='pages',
                                help_text=_(u"Allows to specify the website "
                                            u"which contains the page."))
    parent = models.ForeignKey('self',
                               related_name='children',
                               db_index=True,
                               null=True,
                               blank=True,
                               help_text=_(u"Select the place to add this section."))    
    sha1 =  models.CharField(u'SHA1 Path ID',
                             max_length=40,
                             editable=False,
                             db_index=True)
    
    # -- Page infos

    title = models.CharField(_(u"title"),
                             max_length=255,
                             help_text = _(u'title of the page'))
    slug = models.SlugField(_(u'slug'),
                            blank=True,
                            null=False,
                            help_text=_(u'The section\'s URL. As to be meaningful '
                                          u'and contains only ASCII.'))
    last_modif  = models.DateField(_('last modification'),
                                   auto_now=True)

    # -- Navigation Menu
    is_diplayed_in_menu = models.BooleanField(
        _(u'Main menu'), default=True,
        help_text=_(u"Check if you want to display this section in the main menu."))

    menu_title = models.CharField(_(u"Main menu title"),
                                  max_length=50,
                                  blank=True)

    # -- Application of the page

    app_page_type = models.ForeignKey(ContentType,
                                      limit_choices_to = {'model__startswith': 'pageapp_'},
                                      verbose_name=_("page application"))
    app_page_id = models.PositiveIntegerField(editable=False)
    app_page_object = generic.GenericForeignKey('app_page_type', 'app_page_id')

    placeholder_slug = models.SlugField(_(u'placeholder'),
                                        default='%s1' % (settings.HTML_ID_PLACEHOLDER_CONTENT),
                                        help_text=_(u"Placeholder slug of the page app."))
    plugin_order = models.PositiveIntegerField(_('order'),
                                               default=0,
                                               help_text=_(u"Order of the page app in the placeholder."))

    # -- Meta infos
    meta_keywords = models.CharField(_(u"META Keywords"),
                                     max_length="255",
                                     blank=True)
    meta_description = models.CharField(_(u"META Description"),
                                        max_length="255",
                                        blank=True)
    
    default_template = models.CharField(_(u'template'),
                                        max_length=100, blank=True,
                                        help_text=_(u'Select the theme template for the page.'))
    
    draft = models.BooleanField(_(u'Draft'),
                                default=False,
                                help_text=_(u"Draft are not accessible by visitors but can be edit by administrator."))
    
    @property
    def app(self):
        return self.app_page_object

    def path(self, last_slug=None):
        "Return the complete path of the page."

        if not self.slug:
            return u'/'
        
        parents = self.get_ancestors().filter(slug__isnull=False)
        items = []
        for a in parents:
            slug = getattr(a, 'slug', None)
            if slug is not None:
                items.append(slug)
        items.append(self.slug)
        
        if last_slug:
            items.append(last_slug)

        return u'/%s/' % (u'/'.join(items))


    def __unicode__(self):
        return u'%s : %s' % (self.title, self.path())

    def get_absolute_url(self):
        "Absolute url of the page"
        return self.path()

    @property
    def verbose_name_app(self):
        return self.app_page_object.get_name()

    def get_html_file(self):
        template_list = []
        template_prefix = 'themes/%s/' % self.website.theme
        if self.default_template:
            template_list.append(os.path.join(template_prefix, self.default_template))
        if self.website.default_template:
            template_list.append(os.path.join(template_prefix, self.website.default_template))
        template_list.append(os.path.join(template_prefix, "index.html"))
        return template_list
    html_file = property(get_html_file)
    
    def save(self, *args, **kwargs):
        """
        When we save a page, we are checking its type.
        If it is a new page, we create the page_app
        If it is a update, we check if the type has changed
          if it has changed, we delete the old page_app and create the new one
        Next we generate the SHA1 regarding the page ancestors
        If the slug has changed, we also update children's SHA1
        """
        update_app = False
        # --
        # WARNING :
        # The old app is deleted after that super method save()
        # was called, because deleting app_object lead to
        # deletion of plugin relations.
        old_app_object_to_delete = None
        # --
        # --
        # Deletion of old app page in
        # modification case
        # --
        if self.pk:
            old_page = Page.objects.get(pk__exact=self.pk)
            # We compare the old and new app type
            if self.app_page_type != old_page.app_page_type:
                # Ask deleting the old app instance -- SEE WARNING ABOVE
                old_app_object_to_delete = old_page.app_page_object
                update_app = True
        # --
        # Creation of a new app page if necessary
        # --
        if self.app_page_id is None or update_app:
            AppPageClass = self.app_page_type.model_class()
            new_app = AppPageClass()
            new_app.save()
            self.app_page_id = new_app.pk
        # --
        # Update the SHA1 value
        # --
        if self.parent and self.parent.slug:
            self.sha1 = sha1(self.parent.path(self.slug)).hexdigest()
        else:
            self.parent = None
            self.sha1 = sha1(self.path()).hexdigest()
        saved = super(Page, self).save(*args, **kwargs)

        # --
        # Deleting old app page ?  -- SEE WARNING ABOVE
        if old_app_object_to_delete:
            old_app_object_to_delete.delete()
        # --

        # --
        # Update SHA1 of chidren
        # --
        if self.children:
            for i in self.children.all():
                i.save()
        return saved

    def delete(self):
        """
        This method is called  when one instance is deleted
        (e.g. page manager action), but not necessarily called 
        when deleting objects in bulk using a QuerySet (e.g. django admin).

        Be careful:
        We can't using 'pre_delete' signal because the save() method
        fires the signal... (Django BUG)
        """
        # Deleting App Page
        self.app_page_object.delete()
        # Deleting Plugins - FIX/TODO
        # for plugin_relation in self.plugins.all():
        #     print "Deleting : ", plugin_relation
        #     plugin_relation.content_object.delete()
        # Calling superclass method
        super(Page, self).delete()

    def is_first(self):
        """
            Using MPTT architecture
            If is the first sibling at his level, return True, else return False
        """
        previous = self.get_previous_sibling()
        if previous:
            if previous.slug != '':
                return False
            else:
                return True
        else:
            return True
    
    def is_last(self):
        """
            Using MPTT architecture
            If is the last sibling at his level, return True, else return False
        """
        if self.get_next_sibling():
            return False
        else:
            return True

    def get_meta_keywords(self):
        kw = u''
        if self.website.meta_keywords:
            kw += u'%s' % self.website.meta_keywords
        if self.meta_keywords:
            kw += u', %s' % self.meta_keywords
        return kw

    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        elif self.website.meta_description:
            return self.website.meta_description
        else:
            return u''

    @property
    def is_homepage(self):
        return self.slug == ''


class Layout(models.Model):
    
    slug = models.SlugField(_(u'slug'))
    template = models.CharField(_(u'template file'), max_length=100, blank=True)
    related_object_type = models.ForeignKey(ContentType,
                                            limit_choices_to = {'model__in': ['page', 'website']},
                                            verbose_name=_("related object type"))
    related_object_id = models.PositiveIntegerField(_("related object type"))
    related_object = generic.GenericForeignKey('related_object_type', 'related_object_id')

    def __unicode__(self):
        return u"Layout : %s - %s" % (self.slug, self.template)

    def get_template(self):
        if self.template:
            return self.template
        return settings.LAYOUT_DEFAULT_TEMPLATE

    class Meta:
        verbose_name = _(u'Layout')
        verbose_name_plural = _(u'Layouts')


class AbstractPageApp(models.Model):
    page = generic.GenericRelation(Page,
                                   content_type_field= 'app_page_type',
                                   object_id_field='app_page_id')

    def _get_module_path(self):
        module = self.__module__
        return u'.'.join(module.split('.')[:-1])

    def render_html(self, request):
        "Rendering method of the aplication"
        
        # if settings.DEBUG:
        #     print "## Rendering Application - url requested : ", request.url_app

        # Get the appropriate view
        match = resolve(request.url_app, urlconf=self.get_urlconf())
        # Return the response
        return match.func(request, self, **match.kwargs)

    def get_urlconf(self):
        return self._get_module_path() + u'.urls'

    def get_admin_form(self):
        """
        Returns the default admin form : `PageApp_AppNameForm`.
        """
        class_name = self.__class__.__name__
        forms = __import__('%s.forms' % self._get_module_path(), fromlist=[''])
        try:
            return getattr(forms, '%sForm' % class_name)
        except AttributeError:
            raise PageAppAdminNotProperlyConfiguredError(self)

    def get_actions_urlconf(self):
        return self._get_module_path() + u'.wa_actions_urls'

    def get_sitemap(self):
        return None

    def get_relation_id(self):
        return u'%s%d' % (settings.HTML_ID_APP, self.pk)

    def details(self):
        """
            This method is used in Page Manager to display some details about this page
            For example : Blog - {{ details }} with details = '145 entries'
        """
        return None
    
    def get_absolute_url(self):
        return self.page.get().get_absolute_url()

    @classmethod
    def get_name(cls):
        if hasattr(cls, '_meta'):
            return getattr(cls._meta, 'verbose_name', cls.__name__)
        return cls.__name__


    @classmethod
    def get_description(cls):
        if hasattr(cls, '_meta'):
            return getattr(cls._meta, 'description', '')
        return ''

    class Meta:
        abstract=True



