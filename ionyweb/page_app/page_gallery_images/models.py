# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from ionyweb.page.models import AbstractPageApp


class PageApp_GalleryImages(AbstractPageApp):

    show_album_title = models.BooleanField(
        _(u'Album title displayed'),
        default=True,
        help_text=_(u"The title of album is displayed on the album page."))
    album_title_rule = models.BooleanField(_(u'album title rule'),
                                           default=True)

    @property
    def albums_list(self):
        return self.albums.order_by('order')

    def __unicode__(self):
        return u'Gallery App #%d' % (self.pk)

    class Meta:
        verbose_name = _(u"Gallery App")
        verbose_name_plural = _(u"Gallery Apps")

    class ActionsAdmin:
        title = _(u"Gallery App")
        actions_list = (
            {'title':_(u'Edit albums'), 
             'callback': "admin.page_gallery_images.edit_albums"},
            )

class Album(models.Model):
    app = models.ForeignKey(PageApp_GalleryImages,
                            related_name='albums')
    title = models.CharField(_(u"title"), max_length=100)
    slug = models.SlugField(_(u'slug'), max_length=100, unique=True)
    description = models.TextField(_(u"description"), blank=True)
    order = models.IntegerField(_(u'order'), default=1)

    @property
    def images_list(self):
        return self.images.order_by('order')

    def nb_images(self):
        return self.images_list.count()
    nb_images.action_short_description = _(u'Number of Images')

    def edit_images_action(self):
        return render_to_string('page_gallery_images/actions_admin/action_admin_edit_images.html',
                                {'object': self,
                                 'relation_id': u'%s%d' % (settings.HTML_ID_APP, self.app.id)})
    edit_images_action.action_short_description = ''

    def get_random_image(self):
        try:
            return self.images_list.order_by('?')[0]
        except IndexError:
            return None

    def get_absolute_url(self):
        return u'%sp/album/%s/' % (self.app.get_absolute_url(),
                                    self.slug)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                # Get the last album order of the app
                last_item = list(self.app.albums_list)[-1]
                self.order = last_item.order + 1
            except IndexError:
                self.order = 1
        return super(Album, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        unique_together = ('app', 'slug')
        verbose_name = _(u"Album")
        verbose_name_plural = _(u"Albums")

    class ActionsAdmin:
        title = _(u"Album")
        actions_list = (
            {'title':_(u'Edit'), 'callback': "admin.page_gallery_images.edit_album", 'args':['pk']},
            {'title':_(u'Images'), 'callback': "admin.page_gallery_images.edit_images", 'args':['pk']},
            )


class Image(models.Model):
    
    album = models.ForeignKey(Album, related_name='images')
    image = models.CharField(_("image"), max_length=200)
    title = models.CharField(_(u'title'), max_length=100, blank=True)
    legend = models.TextField(_(u'description'), blank=True)
    order = models.IntegerField(_(u'order'), default=1)

    @property
    def album_pk(self):
        return self.album.pk

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                # Get the last link order of the list
                last_item = list(self.album.images_list)[-1]
                self.order = last_item.order + 1
            except IndexError:
                self.order = 1
        return super(Image, self).save(*args, **kwargs)

    def __unicode__(self):
        return u' %s (%s)' % (self.title, os.path.basename(self.image))

    def get_thumb(self):
        # Dirty trick to get fm_version to work
        website = self.album.app.page.get().website

        return render_to_string('page_gallery_images/actions_admin/action_admin_thumbnail.html',
                                {'path': self.image,
                                 'website': website,
                                 'ADMIN_THUMBNAIL': settings.ADMIN_THUMBNAIL})
    get_thumb.action_short_description=_(u'Thumbnail')

    class Meta:
        verbose_name = _(u'Image')
        verbose_name_plural = _(u'Images')

    class ActionsAdmin:
        title = _(u'Image')
        actions_list = (
            {'title':_(u'Edit'), 'callback': "admin.page_gallery_images.edit_image", 'args':['album_pk', 'pk']},
            )
        related_object = 'album__app'
