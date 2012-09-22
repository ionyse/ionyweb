# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.template.loader import render_to_string

from ionyweb.utils import ContentTypeAccessor as CTA
from ionyweb.website.utils import  main_menus
from ionyweb.page.models import Layout, AbstractPageApp
from ionyweb.plugin.models import PluginRelation
from ionyweb.administration.utils import is_page_placeholder_html_id
from ionyweb.administration.actions.utils import get_actions_for_object_model


class HTMLRendering:
    """
    Basic item which contains informations about
    plugin or app.
    """
    def __init__(self, content, medias=[], title=None):
        self.status_code = 200
        self.content = content
        self.title = title
        self.medias = medias

    def __unicode__(self):
        return self.content


class RenderingItem(object):
    """
    Encapsulate all informations needed to
    render a plugin or app for IonyWeb.

    This object is used by the rendering engine of IonyWeb.
    It give information of the corresponding HTMLRendering object
    and all methods called by the rendering engine.
    """
    def __init__(self, obj, request):
        self._request = request
        self._obj = obj
        self._html_rendering = None
        self._actions = None

    def _init_rendering(self):
        if self.is_app:
            self._html_rendering = self._obj.render_html(self._request)
        else:
            self._html_rendering = self._obj.plugin.render_html(self._request)

    @property
    def is_html_rendering(self):
        return isinstance(self.html_rendering, HTMLRendering)

    @property
    def html_rendering(self):
        if self._html_rendering is None:
            self._init_rendering()
        return self._html_rendering

    @property
    def is_app(self):
        if isinstance(self._obj, AbstractPageApp):
            return True
        return False

    @property
    def html(self):
        return self.html_rendering.content

    @property
    def medias(self):
        return self.html_rendering.medias

    @property
    def title(self):
        return self.html_rendering.title

    def render_complete_html(self, context_instance=None):
        if self.is_app:
            template_file = settings.TEMPLATE_APP
        else:
            template_file = settings.TEMPLATE_PLUGIN
            
        return render_to_string(template_file,
                                {'item': self},
                                context_instance = context_instance)

    @property
    def placeholder_slug(self):
        if self.is_app:
            return self._request.page.placeholder_slug
        else:
            return self._obj.placeholder_slug

    @property
    def layout_slug(self):
        return self.placeholder_slug.split(settings.HTML_ID_PLACEHOLDER)[0]

    @property
    def obj(self):
        return self._obj

    @property
    def html_id(self):
        if self.is_app:
            return '%s%d' % (settings.HTML_ID_APP, self._obj.pk)
        else:
            return '%s%d' % (settings.HTML_ID_PLUGIN, self.obj.pk)

    @property
    def order(self):
        if self.is_app:
            return self._request.page.plugin_order
        else:
            return self._obj.plugin_order

    @property
    def verbose_name(self):
        if self.is_app:
            return self._obj.get_name()
        else:
            return self._obj.plugin.get_name()

    def _get_actions(self):
        if self._actions is None:
            if self.is_app:
                self._actions = get_actions_for_object_model(self._obj)
            else:
                self._actions = get_actions_for_object_model(self._obj.plugin)
        return self._actions

    @property
    def actions_list(self):
        return self._get_actions().get('list', [])

    @property
    def actions_title(self):
        return self._get_actions().get('title', '')

    def __unicode__(self):
        if self.is_app:
            type_obj = u'App'
        else:
            type_obj = u'Plugin'
        return u'RenderingItem - %s (%s): %s' % (type_obj, self.placeholder_slug, self._obj)


class RenderingContext(object):
    """
    Central object of the rendering engine.
    """

    def __init__(self, request, page=None, theme=None):
        self._request = request
        self.page = page
        self.theme = theme
        self._rendering_items = []
        self._medias_set = set()
        self._http_response = None
        self._page_title = []
        # Initialization
        self._populate_rendering_items()

    def _populate_rendering_items(self):
        self._page_title.append(self.page.title)
        if not self._rendering_items:
            # Get the app page
            if self.page.app:
                # We must check if app returns an HttpRedirection
                rendering_app = RenderingItem(self.page.app, self._request)
                self.app = rendering_app
                if rendering_app.is_html_rendering:
                    # Not HTTP Response so we add App
                    # -- Add item in items list
                    self._rendering_items.append(rendering_app)
                    # -- Add medias in medias list
                    self.add_medias(rendering_app.medias)
                    if rendering_app.title is not None:
                        self._page_title.append(rendering_app.title)
                else:
                    self._http_response = rendering_app.html_rendering

            if not self._http_response:
                # Get plugins for the page
                plugin_relations = PluginRelation.objects\
                    .get_plugins_for_page(self.page, self._request.is_admin)
                for plugin_relation in plugin_relations:
                    self.add_item(plugin_relation)

    @property
    def http_response(self):
        return self._http_response

    def set_page(self, page):
        self._page = page
    
    def get_page(self):
        if self._page:
            return self._page
        if self._request:
            return self._request.page
        return None

    def get_website(self):
        if self.page:
            return self.page.website
        return None

    def set_theme(self, theme):
        self._theme = theme

    def get_theme(self):
        if self._theme:
            return self._theme
        else:
            return self.page.website.theme
        
   
    def get_theme_templates(self):
        """
        Return templates files list to use for rendering website.
        
        Templates list is composed by the default page template file,
        the default website template file and finally the `index.html`
        file of the current theme of this object instance.
        """
        template_list = []
        template_prefix = 'themes/%s/' % self.theme
        
        if len(self.theme.split('/')) <= 1:
            template_prefix += "default/"
        
        if self.page.default_template:
            template_list.append(os.path.join(template_prefix, self.page.default_template))
        if self.page.website.default_template:
            template_list.append(os.path.join(template_prefix, self.website.default_template))
        template_list.append(os.path.join(template_prefix, "index.html"))
        return template_list

    def add_item(self, item):
        rendering_item = RenderingItem(item, self._request)
        # TODO : Check if item is not already in items list
        # => Need RenderingItem.__comp__()

        # -- Add item in items list
        self._rendering_items.append(rendering_item)
        # -- Add medias in medias list
        self.add_medias(rendering_item.medias)

        if rendering_item.title is not None:
            self._page_title.append(rendering_item.title)

    def get_items(self, complete_placeholder_slug= None, layout_slug=None, placeholder_slug=None):
        # Make complete placeholder slug if necessary
        if not complete_placeholder_slug and layout_slug and placeholder_slug:
            complete_placeholder_slug = self.get_html_id_placeholder(layout_slug,
                                                                     placeholder_slug)

        items_returned = []
        indices_to_del = []

        for i in xrange(len(self._rendering_items)):
            tmp_item = self._rendering_items[i]
            if tmp_item.placeholder_slug == complete_placeholder_slug:
                # Item is copied to the returned list
                items_returned.append(tmp_item)
                # Indice is added to the del list
                # Be careful : it is necessary to add indices at the
                # front of the list otherwise deleting is compromised.
                indices_to_del.insert(0, i)

        # Del items of value
        for i in indices_to_del:
            del(self._rendering_items[i])
    
        # TODO :
        # Plugins are already sorted, so just insert app
        # at the good index.
        items_returned_sorted = sorted(items_returned, key=lambda x: x.order)

        return items_returned_sorted

    def get_default_items(self):
        return self._rendering_items

    def get_clipboard_items(self):
        return self.get_items(complete_placeholder_slug=settings.HTML_ID_PLACEHOLDER_CLIPBOARD)

    def get_html_id_placeholder(self, layout_slug, placeholder_slug):
        complete_placeholder_slug = u'%s%s%s' % (layout_slug,
                                                 settings.HTML_ID_PLACEHOLDER,
                                                 placeholder_slug)
        return complete_placeholder_slug
    # ------------------
    # LAYOUTS MANAGEMENT
    # ------------------
    def get_layout_templates_files(self, layout_section_slug):
        """
        Return list of layout templates files for a section.
        """
        layout_slug = self.get_layout_template_slug(layout_section_slug)

        # Get template layout file
        layout_templates_files = []
        template_prefix = settings.LAYOUTS_DEFAULT_PATH
        layout_templates_files.append(os.path.join(template_prefix, layout_slug))
        if layout_slug != settings.LAYOUT_DEFAULT:
            layout_templates_files.append(os.path.join(template_prefix, settings.LAYOUT_DEFAULT))
        return layout_templates_files

    def get_layout_template_slug(self, layout_section_slug):
        """
        Returns the specific template slug of the layout page, if exists.
        
        If no layout object defined for the page, returns the settings.LAYOUT_DEFAULT value.
        """
        layout_object = self._get_layout_object(layout_section_slug)
        if layout_object:
            return layout_object.template
        else:
            return settings.LAYOUT_DEFAULT

    def set_layout_template_file(self, layout_section_slug, layout_template_slug):
        # We get existing layout object
        layout_object = self._get_layout_object(layout_section_slug)
        if not layout_object:
            # We create the layout object
            layout_object = Layout(slug=layout_section_slug)
            if is_page_placeholder_html_id(layout_section_slug):
                # Specific case of the layout content section :
                # we bind the layout for this page
                layout_object.related_object_type = CTA().page
                layout_object.related_object_id = self.page.pk
            else:
                layout_object.related_object_type = CTA().website
                layout_object.related_object_id = self.website.pk
        # Global modification
        layout_object.template = layout_template_slug
        layout_object.save()

    def _get_layout_object(self, layout_section_slug):
        # Get layout file for this slug
        # We first try for the page
        try:
            layout_file = Layout.objects.get(slug=layout_section_slug,
                                             related_object_type=CTA().page,
                                             related_object_id=self.page.pk)
        except Layout.DoesNotExist:
            # We try for the website
            try:
                layout_file = Layout.objects.get(slug=layout_section_slug,
                                                 related_object_type=CTA().website,
                                                 related_object_id=self.website.pk)
            except Layout.DoesNotExist:
                layout_file = None
        return layout_file
    # ------------------
    # RENDERING HTML
    # ------------------
    @property
    def is_redirection(self):
        return False

    @property
    def redirection(self):
        return None

    def get_html_placeholder(self, layout_section_slug, id_placeholder, context=None):

        html_id_placeholder = self.get_html_id_placeholder(layout_section_slug, id_placeholder)
        rendering_items = self.get_items(html_id_placeholder)
        return render_to_string(settings.TEMPLATE_PLACEHOLDER,
                                {'ID_PLACEHOLDER' : html_id_placeholder,
                                 'rendering_items': rendering_items},
                                context_instance=context)

    def get_html_layout(self, layout_section_slug, context=None, template_file_preview=None):

        # Preview new layout template
        if template_file_preview:
            template_prefix = settings.LAYOUTS_DEFAULT_PATH
            layout_templates_files = [os.path.join(template_prefix, template_file_preview),
                                      os.path.join(template_prefix, settings.LAYOUT_DEFAULT)]

        else:
            layout_templates_files = self.get_layout_templates_files(layout_section_slug)
        
        if context is None:
            context = RequestContext(self._request)

        html_rendering = render_to_string(layout_templates_files,
                                          {'rendering_context': self,
                                           'layout_slug': layout_section_slug},
                                          context_instance=context)

        return html_rendering

    def refresh_default(self, layout_section_slug, current_default_obj_data=[]):
        
        # Get all items in default of this LAYOUT SECTION
        default_items = filter(lambda x: x.layout_slug == layout_section_slug,
                                   self.get_default_items())

        # Filtering current items in default for the layout section
        current_default_items = filter(
            lambda x: x['layout_slug'] == layout_section_slug,
            current_default_obj_data)

        context_instance = RequestContext(self._request)

        # Add new items in default
        items_to_add = {}
        current_default_items_id = [item['id'] for item in current_default_items]
        for item in default_items:
            if item.html_id not in current_default_items_id:
                items_to_add[item.html_id] = item.render_complete_html(context_instance)

        # Delete the new items of defaults
        items_to_delete = []
        default_items_id = [item.html_id for item in default_items]
        for item in current_default_items:
            if item['id'] not in default_items_id:
                items_to_delete.append(item['id'])

        return {'delete': items_to_delete,
                'add': items_to_add}

    @property
    def html_navigation(self):
        templates = [os.path.join('themes', self._request.website.get_theme(), settings.TEMPLATE_NAV_DEFAULT),
                     os.path.join('themes', settings.TEMPLATE_NAV_DEFAULT)]
        context = main_menus(self._request)
        context['request'] = self._request
        return render_to_string(templates, context)


    def get_html_placeholder_default(self, context=None):
        rendering_items = self.get_default_items()
        return render_to_string(settings.TEMPLATE_PLACEHOLDER_DEFAULT,
                                {'ID_PLACEHOLDER' : settings.HTML_ID_PLACEHOLDER_DEFAULT,
                                 'rendering_items': rendering_items},
                                context_instance=context)
        
    def get_html_placeholder_clipboard(self, context=None):
        rendering_items = self.get_clipboard_items()
        return render_to_string(settings.TEMPLATE_PLACEHOLDER_CLIPBOARD,
                                {'ID_PLACEHOLDER': settings.HTML_ID_PLACEHOLDER_CLIPBOARD,
                                 'rendering_items': rendering_items},
                                context_instance=context)
    # ------------------
    # MEDIAS MANAGEMENT
    # ------------------
    def add_media(self, media):
        if media:
            self._medias_set.add(media)
            
    def add_medias(self, medias=[]):
        try:
            for media in medias:
                self.add_media(media)
        except TypeError:
            pass

    @property
    def medias(self):
        return self._medias_set

    @property
    def html_medias(self):
        rendering_medias = ''
        for media in self.medias:
            rendering_medias += media.render()
        return rendering_medias

    def get_html_medias_for_plugin_relation(self, plugin_relation):
        item = RenderingItem(plugin_relation, self._request)
        html_medias = ''
        for media in item.medias:
            html_medias += media.render()
        return html_medias

    # ------------------
    # PROPERTY
    # ------------------
    page = property(get_page, set_page)
    website = property(get_website)
    theme = property(get_theme, set_theme)
    theme_templates = property(get_theme_templates)

    @property
    def page_title(self):
        title = u' - '.join(self._page_title[::-1])
        return title.replace('<br/>', ' ').replace('<br>', ' ')
    
    def debug(self):
        print u'\n=== RenderingContext : ==='
        print u'Page :', self.page
        print u'Website :', self.website
        print u'Theme :', self.theme
        print u'Theme Templates :', self.theme_templates
        print u'Items :'
        for item in self._rendering_items:
            print unicode(item)
        print u'Medias :'
        for media in self.medias:
            print unicode(media)
        print self.page_title
        print ""
        
