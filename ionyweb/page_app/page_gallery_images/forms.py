# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext as _
import floppyforms as forms

from ionyweb.forms import ModuloModelForm
from ionyweb.widgets import SlugWidget, TinyMCELargeTable
from ionyweb.file_manager.widgets import FileManagerWidget

from models import PageApp_GalleryImages, Album, Image


class PageApp_GalleryImagesForm(ModuloModelForm):

    class Meta:
        model = PageApp_GalleryImages


class AlbumForm(ModuloModelForm):
            
    def render_form(self):
        form = super(AlbumForm, self).render_form()
        if self.instance.pk:
            # Add the Image setup action
            app_html_id = u'%s%d' % (settings.HTML_ID_APP, self.instance.app.pk)
            form += '<tr><th><label>%s :</label></th><td>'\
                '<input type="button" value="%s" '\
                'onClick=\"admin.page_gallery_images.edit_images(\'%s\', \'%s\');"/>'\
                '</td></tr>' % (_(u'Images'), _(u'Edit images'),
                                app_html_id, self.instance.pk)
        return form

    class Meta:
        model = Album
        exclude = ('app', 'order')
        widgets = {
            'slug': SlugWidget('title'),
            'description': TinyMCELargeTable(attrs={'style': 'width: 100%; height: 300px;', }),
            }

class ImageForm(ModuloModelForm):
    
    class Meta:
        model = Image
        exclude = ('album', 'order', 'legend')
        widgets = {
            'image': FileManagerWidget,
            'legend': TinyMCELargeTable(attrs={'style': 'width: 100%; height: 300px;', }),
            }
