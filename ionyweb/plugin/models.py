# -*- coding: utf-8 -*-
import os.path

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.urlresolvers import resolve
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from ionyweb.website.models import WebSite
from ionyweb.page.models import Page
from ionyweb.plugin.exceptions import *
from ionyweb.plugin.settings import PLUGIN

import importlib

class PluginRelationManager(models.Manager):

    def get_plugins_for_page(self, page, clipboard=False):
        """
        Returns plugins relations related to the page.

        If 'clipboard' parameter is True, method returns
        also the clipboard content.
        """
        # Get all plugins related to the page
        page_filter = Q(
            Q(pages=page),
            ~Q(placeholder_slug=settings.HTML_ID_PLACEHOLDER_CLIPBOARD))

        if clipboard:
            # Add all plugins related to the clipboard
            clipboard_filter = Q(
                pages__website=page.website,
                placeholder_slug=settings.HTML_ID_PLACEHOLDER_CLIPBOARD)
            pr_filter = Q(page_filter|clipboard_filter)
        else:
            pr_filter = page_filter

        return super(PluginRelationManager, self).get_query_set()\
            .filter(pr_filter)
        

class PluginRelation(models.Model):

    pages = models.ManyToManyField(Page, related_name="plugins")

    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to = {'model__startswith': 'plugin_'},
                                     verbose_name=_(u"plugin type"))
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    placeholder_slug = models.SlugField(_(u'placeholder'),
                                        #editable=False,
                                        null=False,
                                        blank=True)

    plugin_order = models.PositiveIntegerField(default=0)

    display_on_new_pages = models.BooleanField(_(u'Display on new pages'), default=False)

    objects = PluginRelationManager()

    @property
    def plugin(self):
        return self.content_object

    def __unicode__(self):
        return u"%s - %s : %s" % (self.placeholder_slug, self.plugin_order, self.content_object)

    def delete(self, *args, **kwargs):
        # If the plugin is only on this page, we also delete it.
        signal = (self.pages.count() == 1)
        super(PluginRelation, self).delete(*args, **kwargs)
        if signal:
            self.content_object.delete()

    # def is_in_content(self):
    #     return is_page_placeholder_html_id(self.placeholder_slug)

    class Meta:
        ordering = ['plugin_order']

class AbstractPlugin(models.Model):
    pages = generic.GenericRelation(PluginRelation)

    title = models.CharField(_(u'title'),
                             max_length=100,
                             blank=True,
                             help_text=_(u"Define the title displayed above the plugin."))

    title_rule = models.BooleanField(_(u'display title rule'),
                                     default=True)


    @property
    def template_extra_admin_edit_form(self):
        return os.path.join(self.__module__.split('.')[-1],
                            'admin',
                            'extra_edit_form.html')

    def _get_module_path(self):
        module = self.__module__
        return u'.'.join(module.split('.')[:-1])

    def render_html(self, request):
        """
        Render the html code of the plugin.
        By default, calls the 'index_view' function.
        """
        views = __import__('%s.views' % self._get_module_path(), fromlist=[''])
        try:
            return views.index_view(request, self)
        except AttributeError, e:
            raise e
            raise PluginViewsNotProperlyConfiguredError(self)
        
    def render_html_widget(self, request):
        """
        Render the html code of the plugin.
        By default, calls the 'index_view' function.
        """
        self.template_prefix = settings.TEMPLATE_WIDGET_PREFIX
        return self.render_html(request)

    def get_templates(self, template_name):
        if hasattr(self, 'template_prefix'):
            path_items = template_name.split('/')
            path_items.insert(1, self.template_prefix)
            templates = [os.path.join(*path_items), template_name]
            return templates
        return template_name

    def get_admin_form(self):
        """
        Returns the default admin form : `Plugin_PluginNameForm`.
        """

        class_name = self.__class__.__name__
        forms = __import__('%s.forms' % self._get_module_path(), fromlist=[''])

        try:
            return getattr(forms, '%sForm' % class_name)
        except AttributeError:
            raise PluginAdminNotProperlyConfiguredError(self)

    def get_actions_urlconf(self):
        return self._get_module_path() + u'.wa_actions_urls'

    def get_relation_id(self):
        relation = self.pages.get()
        return u'%s%d' % (settings.HTML_ID_PLUGIN,
                          relation.pk)

    def deepcopy(self, **datas):
        """
        Return a new instance of the plugin.

        You MUST override this method to copy properly your plugin
        in database. For example, you have to ensure that foreigns
        keys and related objects will be duplicated as it shoud be.
        """
        new_obj = self.__class__(**datas)
        new_obj.save()

        return new_obj

    @classmethod
    def get_name(cls):
        if hasattr(cls, '_meta'):
            return getattr(cls._meta, 'verbose_name', cls.__name__)
        return cls.__name__

    @classmethod
    def get_description(cls):
        
        plugin_info = PLUGIN.copy()
        
        # Dynamic call to from ionyweb.plugin_app.plugin_contact import PLUGIN_INFO
        info = importlib.import_module(cls.__module__.rsplit('.',1)[0]).PLUGIN_INFO
        
        plugin_info.update(info)
        
        return plugin_info
    
    class Meta:
        abstract=True
