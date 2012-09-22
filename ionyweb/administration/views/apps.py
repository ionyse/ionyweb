# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.template import RequestContext

from djangorestframework import status
from djangorestframework.response import ErrorResponse, Response

from ionyweb.administration.views import IsAdminView
from ionyweb.administration.utils import MESSAGES, check_placeholder_html_id
from ionyweb.page.models import Page
from ionyweb.website.rendering import RenderingContext


class PageAppView(IsAdminView):
    """
    Managements of the Page App
    """

    def get(self, request, page_pk=None):
        """
        Return the form to edit a app page.
        
        If 'page_pk' parameter is None, returns the edit form
        of the current page (ie request.page),
        else returns the edit form of the page with the id 'page_pk'.
        """
        # Get page with ID 'page_pk'
        if page_pk is not None:
            try:
                page = request.website.pages.select_related()\
                    .get(pk=page_pk)
                app_page = page.app_page_object
            except Page.DoesNotExist:
                raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                    {'msg': MESSAGES.get('default_error', "")})
        else:
            page = request.page
            app_page = request.page.app_page_object
        # Page App Admin Form
        PageAppForm = app_page.get_admin_form()
        form = PageAppForm(instance=app_page)

        data_context = {'form': form,
                        'object': app_page}
        if page_pk:
            data_context['page'] = page

        content = render_to_string('administration/app/app-edit.html',
                                   data_context,
                                   context_instance=RequestContext(request))
        response = Response(status.HTTP_200_OK, {'html': content,})
        return self.render(response)

        
    def post(self, request, page_pk=None):
        """
        Save App Page modifications.

        If correct return confirmation message
        if not, return the form with error messages
        """
        if page_pk is not None:
            try:
                page = request.website.pages.select_related()\
                    .get(pk=page_pk)
                app_page = page.app_page_object
            except Page.DoesNotExist:
                raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                    {'msg': MESSAGES.get('default_error', "")})
        else:
            app_page = request.page.app_page_object
            page = request.page

        # Page App Admin Form
        PageAppForm = app_page.get_admin_form()
        form = PageAppForm(request.POST, instance=app_page)
            
        if form.is_valid():
            new_app_page = form.save()
            # If page is the current page,
            # refresh the layout section
            if request.page == page:
                # Get layout slug
                placeholder_slug_items = check_placeholder_html_id(
                    page.placeholder_slug)
                layout_section_slug = placeholder_slug_items[0]
                # Rendering layout section
                rendering_context = RenderingContext(request)
                html_rendering = rendering_context.get_html_layout(
                    layout_section_slug)
                # Send response
                data_context = {'msg': MESSAGES.get('app_edit_success', ""),
                                'html': html_rendering,
                                'layout_section_slug': layout_section_slug}
                # Check if the page manager have to be displayed
                if page_pk:
                    data_context['refresh_pages_list'] = True
                    
                response = Response(status.HTTP_200_OK,
                                    data_context)
            else:
                data_context = {'msg': MESSAGES.get('app_edit_success', "")}
                # Check if the page manager have to be displayed
                if page_pk:
                    data_context['refresh_pages_list'] = True
                response = Response(status.HTTP_200_OK,
                                    data_context)
            return self.render(response)
            # render_page = page.render_page(request)

            # if render_page.status_code == 200:
            #     response = Response(status.HTTP_200_OK,
            #                         {"msg": MESSAGES.get('app_edit_success', ""),
            #                          'html': render_page.content,
            #                          'medias': render_page.medias})
            # elif render_page.status_code in [301, 302]:
            #     response = Response(status.HTTP_202_ACCEPTED,
            #                         {"msg": MESSAGES.get('redirection', ""),
            #                          'location': render_page['location']})

        # If form not valid => reload the edit form with messages
        else:
            data_context = {'form': form,
                            'object': app_page}
            if page_pk:
                data_context['page'] = page

            html = render_to_string('administration/app/app-edit.html',
                                    data_context,
                                    context_instance=RequestContext(request))
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('invalid_data', ""),
                                 'html': html})
