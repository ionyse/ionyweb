# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status

from ionyweb.utils import ContentTypeAccessor as CTA
from ionyweb.plugin.models import PluginRelation
from ionyweb.website.rendering import RenderingContext
from ionyweb.administration.views import IsAdminView
from ionyweb.administration.utils import (MESSAGES,
                                         check_object_html_id,
                                         check_placeholder_html_id,
                                         is_page_placeholder_html_id)

from ionyweb.plugin.conf import PLUGINS_CATEGORIES, PLUGINS_LIST

class PluginsView(IsAdminView):
    """
    Management of the Plugins List.
    """

    def get(self, request):
        """
        Return the list of available plugin types.

        No parameter required.
        """
        
        html = render_to_string('administration/plugin/plugin-list.html',
                                {'list_plugin': PLUGINS_LIST,
                                 'list_categories': PLUGINS_CATEGORIES},
                                context_instance=RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
class PluginsByCategoryView(IsAdminView):
    """
        Manage category of plugin
    """

    def get(self, request, slug):
        
        list_plugins = PLUGINS_LIST[slug]
        
        html = render_to_string('administration/plugin/plugin-list-by-categories.html',
                                {'list_plugins': list_plugins},
                                context_instance=RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
class PluginsDescription(IsAdminView):

    def get(self, request, id):
        
        plugin = ContentType.objects.get(id=id)
        info = plugin.model_class().get_description()
        
        
        html = render_to_string('administration/plugin/plugin-description.html',
                                {'info': info,
                                 'id': id},
                                context_instance=RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)


class PluginView(IsAdminView):
    """
    Management of the Plugins
    """

    def get(self, request, relation_html_id=None):
        """
        Return plugin form to create or update a plugin.

        If `relation_html_id` is not None, we get the form of
        the existing plugin,else we get an empty form
        in order to create a new plugin.

        Parameters :
          - relation_html_id : Html ID of the plugin relation,
                               e.g. 'plugin-relation-2' where
                               '2' is the PluginRelation ID.

        GET parameters : (required if `pk` is None)
          - placeholder_id : Html ID of the placeholder,
                             e.g. 'content-placeholder-1'.
          - plugin_type    : Content Type ID of the new plugin.
        """
        # ----
        # Get a form of an existing plugin
        # ----
        if relation_html_id is not None:
            # Get the ID relation
            pk = check_object_html_id(relation_html_id)[1]
            try:
                obj = PluginRelation.objects.filter(
                                        pages__website__exact=request.website,
                                        id__exact=pk)[0]
            except IndexError:
                raise Http404
            # Create the plugin form
            plugin = obj.content_object
            PluginFormClass = plugin.get_admin_form()
            form = PluginFormClass(instance=plugin)
            # Get the html of the form
            content = render_to_string('administration/plugin/plugin-edit.html',
                                       {'form': form,
                                        'plugin': plugin,
                                        'plugin_relation_html_id': relation_html_id},
                                       context_instance=RequestContext(request))
            response = Response(status.HTTP_200_OK, {'html': content,})
            return self.render(response)
        # ----
        # Get an empty form to create a new plugin
        # ----
        placeholder_id = request.GET.get('placeholder_id', None)
        plugin_type    = request.GET.get('plugin_type', None)

        if placeholder_id and plugin_type:
            # Check if placeholder ID is valid
            check_placeholder_html_id(placeholder_id)
            try:
                # Get class of the plugin type
                plugin_ct = CTA().get_for_pk(plugin_type)
                PluginClass = plugin_ct.model_class()                
                # Create an empty admin form
                PluginFormClass = PluginClass().get_admin_form()
                plugin_form = PluginFormClass()
                # Get html code of the form
                content = render_to_string('administration/plugin/plugin-create.html',
                                           {'form': plugin_form,
                                            'placeholder_id': placeholder_id,
                                            'plugin_type': plugin_type,},
                                           context_instance=RequestContext(request))
                response = Response(status.HTTP_200_OK, {'html': content,})
                return self.render(response)

            except ContentType.DoesNotExist:
                raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                    {'msg': MESSAGES.get('default_error', "")})
        # Bad parameters => 400
        else:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('default_error', "")})
    
    def put(self, request):
        """
        Create a new plugin.

        If modifications are correct return confirmation message
        and the new render of the layout section;
        if not, return the plugin form with error messages

        PUT parameters :
          - placeholder_id : Html ID of the placeholder, e.g. 'content-placeholder-1'.
          - plugin_type    : Content type ID of the new plugin.
          - form fields
          - csrf token
        """
        # Get PUT parameters
        request.PUT = self.DATA.copy() 

        placeholder_html_id = request.PUT.get('placeholder_id', None)
        plugin_type    = request.PUT.get('plugin_type', None)

        if placeholder_html_id and plugin_type:
            # Check if placeholder ID is valid
            placeholder_slug_items = check_placeholder_html_id(placeholder_html_id)
            layout_section_slug = placeholder_slug_items[0]
            # Get form of the plugin type
            try:
                content_type = CTA().get_for_pk(plugin_type)
            except ContentType.DoesNotExist:
                raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                    {'msg': MESSAGES.get('default_error', "")})

            PluginClass     = content_type.model_class()
            plugin          = PluginClass()
            PluginFormClass = plugin.get_admin_form()
            form            = PluginFormClass(request.PUT, instance=plugin)

            if form.is_valid():
                # Creation of the new plugin
                new_plugin = form.save()
                # Creation of the relation
                display_on_new_pages = (not is_page_placeholder_html_id(placeholder_html_id))
                relation = PluginRelation.objects.create(content_object=new_plugin,
                                                         placeholder_slug= placeholder_html_id,
                                                         display_on_new_pages=display_on_new_pages)
                relation.pages.add(request.page)

                # At the moment, we displayed it on everypage
                if display_on_new_pages:
                    for page in request.website.pages.all():
                        relation.pages.add(page)
                
                # Set right order
                try:
                    last_relation = PluginRelation.objects.filter(
                        pages=request.page,
                        placeholder_slug=placeholder_html_id).order_by('-plugin_order')[0]
                    plugin_order = last_relation.plugin_order + 10
                except IndexError:
                    plugin_order = 0
                relation.plugin_order = plugin_order
                # Saving modifications
                relation.save()

                rendering_context = RenderingContext(request)
                plugin_html_medias = rendering_context\
                    .get_html_medias_for_plugin_relation(relation)
                html_rendering = rendering_context.get_html_layout(layout_section_slug)
                
                # Sending response
                response = Response(status.HTTP_200_OK,
                                    {'msg': MESSAGES.get('item_edit_success', ''),
                                     'html': html_rendering,
                                     'layout_section_slug': layout_section_slug,
                                     'medias': plugin_html_medias})
                return self.render(response)
            
            # Invalid Form => 400 BAD REQUEST
            else:
                html = render_to_string('administration/plugin/plugin-create.html',
                                        {'form': form,
                                         'placeholder_id': placeholder_html_id,
                                         'plugin_type': plugin_type},
                                       context_instance=RequestContext(request))
                raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                    {'msg': MESSAGES.get('invalid_data', ""),
                                     'html': html})
        # Bad parameters => 400 BAD REQUEST
        else:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('default_error', "")})

    def post(self, request, relation_html_id):
        """
        Update plugin modifications.

        If modifications are correct return confirmation message
        and the new render of the layout section;
        if not, return the plugin form with error messages

        Parameters :
          - relation_html_id : PluginRelation Id

        POST parameters :
          - form fields
          - csrf token
        """
        pk = check_object_html_id(relation_html_id)[1]
        try:
            plugin_relation = PluginRelation.objects.filter(
                pages__website__exact=request.website, 
                id__exact=pk)[0]
        except IndexError:
            raise Http404
        # Create the plugin form
        plugin = plugin_relation.content_object
        PluginFormClass = plugin.get_admin_form()
        form = PluginFormClass(request.POST, instance=plugin)

        if form.is_valid():
            plugin = form.save()
            placeholder_slug_items = check_placeholder_html_id(
                plugin_relation.placeholder_slug)
            layout_section_slug = placeholder_slug_items[0]
            rendering_context = RenderingContext(request)
            html_rendering = rendering_context.get_html_layout(layout_section_slug)

            response = Response(status.HTTP_200_OK,
                                {"msg": MESSAGES.get('item_edit_success',""),
                                 'html': html_rendering,
                                 'layout_section_slug': layout_section_slug})

            return self.render(response)
        
        else:            
            # Invalid form => 400 BAD REQUEST
            # with forms (and errors..)
            html = render_to_string('administration/plugin/plugin-edit.html',
                                    {'form': form,
                                     'plugin': plugin,
                                     'plugin_relation_html_id': relation_html_id},
                                    context_instance = RequestContext(request))
            
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('invalid_data', ""),
                                 'html': html})

    def delete(self, request, relation_html_id):
        """
        Delete a plugin.

        Parameters :
          - pk : PluginRelation.id.
        """

        pk = check_object_html_id(relation_html_id)[1]

        try:
            obj = PluginRelation.objects.filter(pages__website__exact=request.website, 
                                                id__exact=pk)[0]
        except IndexError:
            raise Http404

        obj.delete()
        
        response = Response(status.HTTP_200_OK,
                            {"msg": MESSAGES.get('plugin_delete_success', '')})
        return self.render(response)    
        


class PluginRelationView(IsAdminView):
    """
    Management of the PluginRelation.
    """
    
    def post(self, request):
        """
        Update a PluginRelation.

        Parameters :
          - placeholder_id : HTML ID of the new placeholder, eg "content-placeholder-1"
          - plugins_order[] : Ordered list of plugins HTML IDs in the new placeholder
        """
        
        placeholder_html_id = request.POST.get('placeholder_id', None)
        plugins_order  = request.POST.getlist('plugins_order[]')

        if placeholder_html_id and plugins_order:

            # Check placeholder HTML ID
            check_placeholder_html_id(placeholder_html_id,
                                      extras_id=[settings.HTML_ID_PLACEHOLDER_CLIPBOARD,])

            i = 0
            for plugin_id in plugins_order:                
                # Check plugin HTML ID
                plugin_type, relation_id = check_object_html_id(plugin_id,
                                                           types=[settings.SLUG_PLUGIN,
                                                                  settings.SLUG_APP])

                # Be careful, can be a Page object or a relation object
                # In case you are moving the app and not a plugin
                if plugin_type == settings.SLUG_APP:
                    if placeholder_html_id == settings.HTML_ID_PLACEHOLDER_CLIPBOARD:
                        raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                            {'msg': MESSAGES.get('default_error', "")})
                    # Get page object to manage app order
                    obj = request.page
                # Plugin object
                else:
                    try:
                        obj = PluginRelation.objects.filter(pages__website__exact=request.website, 
                                                            id__exact=relation_id)[0]

                        # 1. This new placeholder_html_id is website placeholder
                        #      - Add all pages
                        #      - Activate auto creation on new pages
                        if not (is_page_placeholder_html_id(placeholder_html_id) or 
                                placeholder_html_id == settings.HTML_ID_PLACEHOLDER_CLIPBOARD):
                            obj.pages.add(*request.website.pages.all())
                            if not obj.display_on_new_pages:
                                obj.display_on_new_pages = True
                                obj.save()

                        else:
                        # 2. This new placeholder_html_id is page placeholder
                        #      - Delete all pages
                        #      - Add current pages
                        #      - Deactivate auto creation in new page
                            obj.pages.clear()
                            obj.pages.add(request.page)
                            if obj.display_on_new_pages:
                                obj.display_on_new_pages = False
                                obj.save()
                    except IndexError:
                        raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                            {'msg': MESSAGES.get('default_error', "")})
                # Update order
                obj.plugin_order = i
                if plugin_type == settings.SLUG_APP:
                    if i > 5:
                        obj.plugin_order -= 5
                else:
                    i = i + 10
                # Update placeholder slug
                obj.placeholder_slug = placeholder_html_id
                obj.save()
            # Send a 200 Response
            response = Response(status.HTTP_200_OK,
                                {"msg": MESSAGES.get('items_move_success', '')})
            return self.render(response)

        # Bad parameters => 400 BAR REQUEST
        else:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('default_error', "")})

