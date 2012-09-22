# -*- coding: utf-8 -*-
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from ionyweb.plugin.models import AbstractPlugin
from ionyweb.settings import VERSIONS


class Plugin_Image(AbstractPlugin):

    ALIGNMENT_CHOICES = (
        ('C', _(u'Centre')),
        ('L', _(u'Left')),
        ('R', _(u'Right')),
        )

    image = models.CharField(_(u'File'),
                             max_length=255)


    description = models.CharField(_(u'description'),
                                   max_length=255,
                                   blank=True)

    width = models.PositiveIntegerField(_(u"width"),
                                        blank=True,
                                        null=True)

    height = models.PositiveIntegerField(_(u"height"),
                                         blank=True,
                                         null=True)
    
    lightbox = models.BooleanField(_('show lightbox'),
                                   default=True)

    alignment = models.CharField(_('alignment'), max_length=1,
                                 choices=ALIGNMENT_CHOICES,
                                 default='C')

    def __unicode__(self):
        return u'Image #%d : %s' % (self.pk, self.image)

    @property
    def file_name(self):
        if self.image:
            try:
                return self.image.split('/')[-1]
            except IndexError:
                pass
        return ''

    @property
    def original_file(self):
        """
        Returns path of original file (whitout version suffix).
        """
        file_path = self.image
        file_path, ext = file_path.rsplit('.', 1)
        file_path, suffix_version = file_path.rsplit('_', 1)
        if suffix_version in VERSIONS.keys():
            return u'%s.%s' % (file_path, ext)
        return self.image

    class Meta:
        verbose_name = ugettext(u"Image")
