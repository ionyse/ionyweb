# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import RequestContext
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.base import TemplateResponseMixin

from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status

from ionyweb.website.rendering import RenderingContext
from ionyweb.page.models import AbstractPageApp
from ionyweb.plugin.models import AbstractPlugin
from ionyweb.administration.views import IsAdminView
from ionyweb.administration.utils import MESSAGES, check_object_html_id, check_placeholder_html_id


class ActionAdminListView(ListView, IsAdminView):

    template_name = 'actions_admin/change_list.html'
    obj_field = None
    ordering = None
    sortable = None
    sortable_field = 'order'
    list_display = None

    def get_model(self):
        if self.model is not None:
            return self.model
        else:
            raise ImproperlyConfigured(u"'%s' must define 'model'"
                                       % self.__class__.__name__)

    def get_obj_field(self, obj):
        if self.obj_field is not None:
            return self.obj_field

        if isinstance(obj, AbstractPageApp):
            return 'app'

        if isinstance(obj, AbstractPlugin):
            return 'plugin'

        raise ImproperlyConfigured(u"'%s' must define an 'obj_field' attribute"
                                   % self.__class__.__name__)

    def get_queryset(self, obj):
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(u"'%s' must define 'queryset' or 'model'"
                                       % self.__class__.__name__)

        if hasattr(queryset, 'using_translations'):
            queryset = queryset.using_translations()

        obj_field = self.get_obj_field(obj)
        if hasattr(self.get_model(), obj_field):
            extra_filter = {obj_field: obj}
            queryset = queryset.filter(**extra_filter)

        # Sortable Items
        if self.sortable:
            queryset = queryset.order_by(self.sortable_field)
        else:
            # Ordering Items
            if self.ordering:
                if isinstance(self.ordering, tuple) \
                        or isinstance(self.ordering, list):
                    queryset = queryset.order_by(*self.ordering)
                else:
                    queryset = queryset.order_by(self.ordering)
            else:
                # If no specific ordering, we try to use default Meta.ordering field.
                try:
                    meta_ordering = self.model._meta.ordering
                except AttributeError:
                    # Else we order by the primary key
                    meta_ordering = None
                if meta_ordering:
                    queryset = queryset.order_by(*meta_ordering)
                else:
                    queryset = queryset.order_by('pk')
        return queryset
        
    
    def get(self, request, relation_id, app_obj, object_pk=None, *args, **kwargs):

        self.object_list = self.get_queryset(app_obj)
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


    def render_to_response(self, context):
        
        content = render_to_string(self.get_template_names(),
                                   context,
                                   context_instance=RequestContext(self.request))
        response = Response(status.HTTP_200_OK,
                            {'html': content})
        return self.render(response)
     
    def get_context_data(self, **kwargs):
        
        context = super(ActionAdminListView, self).get_context_data(**kwargs)
        
        model = self.get_model()
        context['verbose_name'] = model._meta.verbose_name
        context['verbose_name_plural'] = model._meta.verbose_name_plural
        context['sortable'] = self.sortable
        # List Display Field
        if self.list_display:
            list_display_title = []
            for attr in self.list_display:
                # We first try in attribute (methods of model).
                try:
                    attr_obj = getattr(model, attr)
                    if hasattr(attr_obj, 'action_short_description'):
                        desc = getattr(attr_obj, 'action_short_description')
                    elif hasattr(attr_obj, 'short_description'):
                        desc = getattr(attr_obj, 'short_description')
                    else:
                        desc = attr_obj.__func__.__name__
                except AttributeError:
                    # We now check in model fields
                    if hasattr(model._meta, 'translations_model') and \
                            attr in model._meta.translations_model._meta.get_all_field_names():
                        desc = model._meta.translations_model._meta.get_field(attr).verbose_name
                    elif attr in model._meta.get_all_field_names():
                        desc = model._meta.get_field(attr).verbose_name
                    else:
                        raise ValueError(_(u"Caught ImproperlyConfigured while rendering: "
                                           u"ActionAdminListView.list_display, '%(attr)s' is not a "
                                           u"callable or an attribute of the model '%(model)s'.") \
                                             % {'attr': attr, 'model': model})
                list_display_title.append(desc)
            context['list_display_title'] = list_display_title
            context['list_display'] = self.list_display
        return context



class RefreshPlaceholderView():
    """
    Defines interface which allow to return
    response with automatic refresh of current placeholder.
    """
    def render_to_response_with_refresh(self, relation_id, app_obj, msg=None):
        
        id_items = check_object_html_id(relation_id,
                                        types=[settings.SLUG_PLUGIN,
                                               settings.SLUG_APP])
        # APP rendering
        if id_items[0] == settings.SLUG_APP:
            # Get placeholder slug in page
            placeholder_slug = app_obj.page.get().placeholder_slug
        # Plugin Rendering
        else:
            # Get placeholder_slug in relation
            placeholder_slug = app_obj.pages.get(pages=self.request.page).placeholder_slug

        placeholder_slug_items = check_placeholder_html_id(placeholder_slug)
        layout_section_slug = placeholder_slug_items[0]
        placeholder_id = placeholder_slug_items[2]
        rendering_context = RenderingContext(self.request)
        html = rendering_context.get_html_placeholder(layout_section_slug, placeholder_id,
                                                      context=RequestContext(self.request))
        datas = {'html': html, 'placeholder_slug': placeholder_slug}
        if msg:
            datas['msg'] = msg
        response = Response(status.HTTP_200_OK, datas)
        return self.render(response)



class ActionAdminDetailView(IsAdminView, RefreshPlaceholderView, ModelFormMixin, TemplateResponseMixin):

    template_name = 'actions_admin/change_form.html'
    obj_field = None
    initial_data = {}
    field_to_app_filter = None

    def get_model(self):
        if self.model is not None:
            return self.model
        else:
            raise ImproperlyConfigured(u"'%s' must define 'model'"
                                       % self.__class__.__name__)

    def get_initial(self):
        """
        Remove conflict between django-rest-framework and FormMixin
        """
        return self.initial_data
        
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.DATA,
                'files': self.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        
        context = super(ActionAdminDetailView, self).get_context_data(**kwargs)
        
        context['verbose_name'] = self.get_model()._meta.verbose_name
        context['verbose_name_plural'] = self.get_model()._meta.verbose_name_plural
        context['module_name'] = self.get_model()._meta.module_name

        return context

    def get_obj_field(self, obj):
        if self.obj_field is not None:
            return self.obj_field

        if isinstance(obj, AbstractPageApp):
            return 'app'

        if isinstance(obj, AbstractPlugin):
            return 'plugin'

        raise ImproperlyConfigured(u"'%s' must define an 'obj_field' attribute"
                                   % self.__class__.__name__)
    
    def get_new_form(self, *args, **kwargs):
        FormClass = self.get_form_class()
        if 'app_obj' in kwargs:
            del kwargs['app_obj']
        return FormClass(*args, **kwargs)

    def get_edit_form(self, *args, **kwargs):
        if 'app_obj' in kwargs:
            del kwargs['app_obj']
        form_kwargs = self.get_form_kwargs()
        form_kwargs.update(kwargs)
        return self.get_form_class()(*args, **form_kwargs)

    def render_to_response(self, context, status_code=status.HTTP_200_OK, msg=None):
        content = render_to_string(self.get_template_names(),
                                   context,
                                   context_instance=RequestContext(self.request))
                         
        datas = {'html': content}
        if msg is not None:
            datas['msg'] = msg

        response = Response(status_code, datas)
        return self.render(response)
        

    def get(self, request, relation_id, app_obj, object_pk=None, *args, **kwargs):
        """
        Return a form for model object.
        
        If 'pk' is not None, return the edition form, else,
        return a creation form for the object.

        """
        self.kwargs['pk'] = object_pk

        add_view = False
        
        if object_pk is not None:
            FormClass = self.get_form_class()
            self.object = self.get_object()
            form = self.get_new_form(instance=self.object, app_obj=app_obj)
        else:
            self.object = None
            form = self.get_new_form(app_obj=app_obj)
            add_view = True

        extra_context = {'form': form,
                         'add': add_view}

        return self.render_to_response(self.get_context_data(**extra_context))


    def put(self, request, relation_id, app_obj, object_pk=None, *args, **kwargs):
        self.object = None

        form = self.get_edit_form(*args, app_obj=app_obj)

        if form.is_valid():
            obj = form.save(commit=False)
            field_name = '%s_id' % self.get_obj_field(app_obj)
            if hasattr(obj, field_name):
                setattr(obj, field_name, app_obj.pk)
            form.save()
            # Refresh placeholder
            return self.render_to_response_with_refresh(relation_id,
                                                        app_obj,
                                                        msg=MESSAGES.get('item_creation_success', ''))
    
        else:
            extra_context = {'form': form,
                             'add': True}
            return self.render_to_response(self.get_context_data(**extra_context),
                                           status_code=status.HTTP_400_BAD_REQUEST,
                                           msg=MESSAGES.get('invalid_data', ''))


    def post(self, request, relation_id, app_obj, object_pk, *args, **kwargs):
        self.kwargs['pk'] = object_pk
        self.object = self.get_object()

        # If the current path of the page is concerned by the edited object
        check_redirection = False
        if hasattr(self.object, 'get_absolute_url'):
            obj_abs_url_before_edit = self.object.get_absolute_url()
            complete_page_url = request.path_info.split(settings.URL_ADMIN_SEP)[0]
            if complete_page_url == obj_abs_url_before_edit:
                check_redirection = True

        form = self.get_edit_form(instance=self.object, app_obj=app_obj)
        if form.is_valid():
            form.save()
            
            if check_redirection:
                # We must check if redirection is needed
                obj_abs_url_after_edit = self.object.get_absolute_url()
                if obj_abs_url_before_edit != obj_abs_url_after_edit:
                    # The absolute url object was changed, so reload page
                    response = Response(status.HTTP_202_ACCEPTED,
                                        {"msg": MESSAGES.get('redirection', ""),
                                         'location': obj_abs_url_after_edit})
                    return self.render(response)

            # Response with refresh placeholder
            return self.render_to_response_with_refresh(relation_id,
                                                        app_obj,
                                                        msg=MESSAGES.get('item_edit_success', ''))
        else:
            extra_context = {'form': form,
                             'add': False}
            return self.render_to_response(self.get_context_data(**extra_context),
                                           status_code=status.HTTP_400_BAD_REQUEST,
                                           msg=MESSAGES.get('invalid_data', ''))

    def delete(self, request, relation_id, app_obj, object_pk, *args, **kwargs):
        Model = self.get_model()
        try:
            obj = Model.objects.get(pk=object_pk)
        except Model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND,
                                {'msg': MESSAGES.get('default_error', '')})
        else:
            obj.delete()
            return self.render_to_response_with_refresh(relation_id,
                                                        app_obj,
                                                        msg=MESSAGES.get('item_delete_success', ''))


class ActionAdminOrderView(IsAdminView, RefreshPlaceholderView):
    model = None
    sortable_field = 'order'

    def get_model(self):
        if self.model is not None:
            return self.model
        else:
            raise ImproperlyConfigured(u"'%s' must define 'model'"
                                       % self.__class__.__name__)

    def get_object(self, pk):
        if self.model is not None:
            try:
                return self.model._default_manager.get(pk=pk)
            except self.model.DoesNotExist:
                return None
        else:
            raise ImproperlyConfigured(u"'%s' must define 'queryset' or 'model'"
                                       % self.__class__.__name__)

    def post(self, request, relation_id, app_obj, action_obj_pk=None, *args, **kwargs):
        objects_order  = request.POST.getlist('action_objects_order[]')
        order = 1
        for object_id in objects_order:
            object_pk = object_id.split('action-object-')[1]
            obj = self.get_object(object_pk)
            try:
                setattr(obj, self.sortable_field, order)
            except AttributeError:
                raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                    {'msg': MESSAGES.get('default_error', "")})
            obj.save()
            order += 1
            
        return self.render_to_response_with_refresh(relation_id,
                                                    app_obj,
                                                    msg=MESSAGES.get('item_edit_success', ''))
