# -*- coding: utf-8 -*-

from ionyweb.administration.views import IsAdminView
from djangorestframework.response import Response
from djangorestframework import status

# from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext

from ionyweb.utils import ContentTypeAccessor as CTA
from ionyweb.plugin.models import PluginRelation
from ionyweb.page.forms import PageWAForm
from ionyweb.administration.utils import MESSAGES
from ionyweb.website.rendering import RenderingContext

class PagesView(IsAdminView):
    """
    Return a list of all pages installed
    """
    def get(self, request):
        """
        Return the list of pages
        """
        pages = request.website.pages.all()
        html = render_to_string('administration/page/page-list.html',
                                {'pages': pages,},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)

# class PageContentView(IsAdminView):
#     """
#     Return the content of #main-content in HTML. Use mainly for ajax update
#     """
    
#     def get(self, request):
#         response = Response(status.HTTP_200_OK, {"html": request.page.render_page(request).content,
#                                                  'css_file': request.page.get_layout_css_file(), })
#         return self.render(response)

#
# class PageDuplicateView(IsAdminView):
# DON'T USE DEEPCOPY BUT DO IT HERE
#     def get(self, request, pk=None):
#         if pk:
#             page = get_object_or_404(request.website.pages, pk=pk)
#             new_page = page.deepcopy()
#         else:
#             raise Http404
        
#         pages = request.website.pages.all()
#         html = render_to_string('administration/page/page-list.html',
#                                     {'pages': pages,},
#                                     context_instance = RequestContext(request))
        
#         response = Response(status.HTTP_200_OK,
#                             {"html": html})
#         return self.render(response)   
    


class PageLayoutView(IsAdminView):

    def get(self, request):

        layout_section_slug = request.GET.get('layout_section_slug', None)

        if not layout_section_slug:            
            response = Response(status.HTTP_400_BAD_REQUEST,
                                {"msg": MESSAGES.get('default_error', "")})
            return self.render(response)

        rendering_context = RenderingContext(request)
        html_rendering = rendering_context.get_html_layout(layout_section_slug)

        response = Response(status.HTTP_200_OK,
                            {'html': html_rendering,
                             'msg': MESSAGES.get('items_edit_success', "")})

        return self.render(response)



class PageSelectApp(IsAdminView):
    pass

class PageView(IsAdminView):
    """
    Modify a Page object
    """

    def get(self, request, pk=None):
        """
        Return creation or edition form if pk is provided
        """
        if pk is None:
            default_data = {'app_page_type': CTA().get_for_names("page_text", "pageapp_text")}

            if 'parent' in request.GET and request.GET['parent'] != '0':
                default_data['parent'] = request.GET['parent']
            form = PageWAForm(initial=default_data)
                
            html = render_to_string('administration/page/page-create.html',
                                    {'form': form,},
                                    context_instance = RequestContext(request))

            response = Response(status.HTTP_200_OK, {"html": html})
            return self.render(response)
        else:
            page = get_object_or_404(request.website.pages, pk=pk)
            form = PageWAForm(instance=page)
            html = render_to_string('administration/page/page-edit.html',
                                    {'form': form, 
                                     'page': page},
                                    context_instance = RequestContext(request))
            response = Response(status.HTTP_200_OK, {"html": html})
            return self.render(response)
        
    def put(self, request, pk=None):
        post_values = self.DATA.copy()
        post_values['website'] = request.website.id
        form = PageWAForm(post_values)
        if form.is_valid():
            page = form.save()

            # Add the new page on auto_display PluginRelation
            plugins_relation = PluginRelation.objects.filter(display_on_new_pages=True, pages__website=request.website)

            for plugin_relation in plugins_relation:
                plugin_relation.pages.add(page)

            response = Response(status.HTTP_202_ACCEPTED,
                                {"msg": MESSAGES.get('redirection', ""),
                                 'location': page.get_absolute_url()})
        else:
            content = render_to_string('administration/page/page-create.html',
                                    {'form': form,},
                                    context_instance = RequestContext(request))
            response = Response(status.HTTP_400_BAD_REQUEST,
                                {"html": content,
                                 "msg": MESSAGES.get('default_error', "")})
        return self.render(response)

    def post(self, request, pk):
        """
        Modify the page
        """
        # Get page which is currently updated
        page = get_object_or_404(request.website.pages, pk=pk)
        # Saving url of current page
        old_url_current_page = request.page.get_absolute_url()
        # Settings Refresh
        refresh_manager = False
        refresh_page = False
        msg_user = None
        # ----------------------
        # Moving Page Management
        # ----------------------
        if 'move' in request.POST:
            if 'previous' in request.POST:
                page_top = get_object_or_404(request.website.pages, pk=request.POST['previous'])
                page.move_to(page_top, 'right')
            else:
                if 'next' in request.POST:
                    page_top = get_object_or_404(request.website.pages, pk=request.POST['next'])
                    page.move_to(page_top, 'left')
                else:
                    if 'parent' in request.POST:
                        page_top = get_object_or_404(request.website.pages, pk=request.POST['parent'])
                        page.move_to(page_top, 'first-child')
            # We save updates.
            page.save()
            # Ask refresh manager
            refresh_manager = True
            # Messgae fo user
            msg_user = MESSAGES.get('items_move_success', '')
        # ----------------------
        # Settings page as draft
        # ----------------------
        elif 'draft' in request.POST:
            page.draft = not page.draft
            page.save()
            refresh_manager = True
            msg_user = MESSAGES.get('page_draft_toggle', '') 
        # ----------------------
        # Updating settings page
        # ----------------------
        else:
            # Get POST values
            post_values = request.POST.copy()
            post_values['website'] = request.website.id
            # Creation of form
            form = PageWAForm(post_values, instance=page)
            if form.is_valid():
                page = form.save()
                # We ask content updating
                if page == request.page:
                    refresh_page = True
                # Message for user
                msg_user = MESSAGES.get('app_edit_success', '')
            else:
                # We reload the edit form with errors
                content = render_to_string('administration/page/page-edit.html',
                                           {'form': form, 
                                            'page': page},
                                           context_instance = RequestContext(request))
                response = Response(status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                                    {"html": content,
                                     "msg": MESSAGES.get('default_error', "")})
                return self.render(response)
        # ---------------
        # Refresh Website
        # ---------------
        # Update cache for current page displayed.
        request.page = get_object_or_404(request.website.pages, pk=request.page.id)
        # Check if we need reload current page
        # if current url changed or refresh content asked.
        new_url_current_page = request.page.get_absolute_url()
        if old_url_current_page != new_url_current_page or refresh_page:
            response = Response(status.HTTP_202_ACCEPTED,
                                {'location': new_url_current_page})
            return self.render(response)
        # Else we refresh only page manager and navigation.
        # Page manager:
        if refresh_manager:
            pages_list = request.website.pages.all()
            page_manager_html = render_to_string('administration/page/page-list.html',
                                                 {'pages': pages_list,},
                                                 context_instance = RequestContext(request))
        else:
            page_manager_html = None

        navigation_html = RenderingContext(request).html_navigation
        # Response
        response = Response(status.HTTP_200_OK,
                            {"manager_html": page_manager_html,
                             "navigation_html": navigation_html,
                             # "page_html": page_content_html,
                             "msg": msg_user})
        return self.render(response)

    def delete(self, request, pk):
        page = get_object_or_404(request.website.pages, pk=pk)
        url_home_page = request.website.get_url_home_page()

        # We can't delete the home page
        if page.get_absolute_url() == url_home_page:
            response = Response(status.HTTP_400_BAD_REQUEST,
                                {"msg": MESSAGES.get('delete_home_page_error', "")})
            return self.render(response)
        # Need redirection if page is currently displayed
        if request.page == page:
            redirection = True
        else:
            redirection = False
        # Deleting page
        page.delete()
        # Make response
        if redirection:
            response = Response(status.HTTP_202_ACCEPTED, {'location': url_home_page})
        else:
            # Refresh Menu navigation:
            navigation_html = RenderingContext(request).html_navigation
            response = Response(status.HTTP_200_OK,
                                {"id": pk,
                                 "navigation_html": navigation_html,
                                 "msg": MESSAGES.get('page_delete_success', "")})
        # Send response
        return self.render(response)
