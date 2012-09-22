# -*- coding: utf-8 -*-
from djangorestframework.response import Response
from djangorestframework import status

from ionyweb.administration.actions.views import ActionAdminListView, ActionAdminDetailView
from ionyweb.administration.utils import MESSAGES

from ionyweb.page_app.page_gallery_images.models import Image, Album
from ionyweb.page_app.page_gallery_images.forms import ImageForm


class ImageActionAdminListView(ActionAdminListView):
    template_name = 'page_gallery_images/actions_admin/change_list.html'
    model = Image

    def get(self, request, relation_id, app_obj, object_pk=None, *args, **kwargs):
        try:
            album_pk = kwargs['album_pk']
            self.album = Album.objects.get(pk=kwargs['album_pk'])
        except (KeyError, Album.DoesNotExist):
            self.album = None
        return super(ImageActionAdminListView, self).get(request, relation_id, app_obj, object_pk)

    def get_context_data(self, **kwargs):
        context = super(ImageActionAdminListView, self).get_context_data(**kwargs)
        context['album'] = self.album
        return context

    def get_queryset(self, obj):
        queryset = super(ImageActionAdminListView, self).get_queryset(obj)
        if self.album:
            queryset = queryset.filter(album=self.album)
        return queryset

class ImageActionAdminDetailView(ActionAdminDetailView):
    model = Image
    form_class = ImageForm

    def put(self, request, relation_id, app_obj, object_pk=None, *args, **kwargs):
        self.object = None
        form = self.get_form_class()(**self.get_form_kwargs())
        if form.is_valid():
            obj = form.save(commit=False)
            obj.album = Album.objects.get(pk=kwargs['album_pk'])
            form.save()
            return self.render_to_response_with_refresh(relation_id,
                                                        app_obj,
                                                        msg=MESSAGES.get('item_creation_success', ''))
        else:
            extra_context = {'form': form,
                             'add': True}
            return self.render_to_response(self.get_context_data(**extra_context),
                                           status_code=status.HTTP_400_BAD_REQUEST,
                                           msg=MESSAGES.get('invalid_data', ''))
