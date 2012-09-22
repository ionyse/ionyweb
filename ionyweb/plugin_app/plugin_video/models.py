# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from ionyweb.plugin.models import AbstractPlugin

from ionyweb.plugin_app.plugin_video.viewers import (YoutubeViewer, 
                                                    DailymotionViewer,
                                                    VimeoViewer,
                                                    FacebookViewer)

VIDEO_VIEWERS = getattr(settings, 'PLUGIN_VIDEO_VIEWERS' , 
                          {'D': DailymotionViewer,
                           'Y': YoutubeViewer,
                           'V': VimeoViewer,
                           'F': FacebookViewer})

VIDEO_TYPE_CHOICES = [(i[0], i[1].__name__.replace('Viewer', '')) for i in  VIDEO_VIEWERS.items()]

class Plugin_Video(AbstractPlugin):

    MAX_WIDTH_VIDEO = 1920
    MAX_HEIGHT_VIDEO = 1080
    PREFERRED_HEIGHT_VIDEO = 350

    video_type = models.CharField(_(u"type"),
                                  max_length=1,
                                  choices=VIDEO_TYPE_CHOICES)
    
    id_video = models.CharField(_(u"id"),
                                max_length=200)

    description = models.CharField(_(u'description'),
                                   max_length=255,
                                   blank=True)

    url = models.URLField(_(u"URL"),
                          max_length=255,
                          verify_exists=True,
                          help_text=_(u"Copy/Paste the video URL.<br/>"
                                      u"You can paste a YouTube, Dailymotion or Vimeo video URL."))

    width_video = models.PositiveIntegerField(_(u"width"),
                                              blank=True,
                                              null=True,
                                              help_text=_(u"You can set the video width in pixels.<br/>"
                                                          u"By default, the video will take 100%% of "
                                                          u"length available. "
                                                          u"Max width : %(size)s px.") % {'size': MAX_WIDTH_VIDEO})

    height_video = models.PositiveIntegerField(_(u"height"),
                                               blank=True,
                                               null=True,
                                               help_text=_(u"You can set the video height in pixels.<br/>"
                                                           u"By default, the height will be 80%% of "
                                                           u"the width if set, "
                                                           u"or %(size)s px otherwise. Max height: %(max)s px.") % 
                                               {'size': PREFERRED_HEIGHT_VIDEO, 'max': MAX_HEIGHT_VIDEO})

    @property
    def width(self):
        if self.width_video:
            return min(self.width_video, self.MAX_WIDTH_VIDEO)
        return None

    @property
    def height(self):
        if self.height_video:
            return min(self.height_video, self.MAX_HEIGHT_VIDEO)
        if self.width:
            return min(int(self.width_video * 0.8), self.MAX_HEIGHT_VIDEO)
        return self.PREFERRED_HEIGHT_VIDEO

    @property
    def viewer(self):
        if self.video_type in VIDEO_VIEWERS.keys():
            return VIDEO_VIEWERS[self.video_type].get_video_viewer(self.id_video)
        else:
            raise NotImplementedError('Viewer type not found in settings.PLUGIN_VIDEO_VIEWER : "%s"' % self.video_type)

    def __unicode__(self):
        return u'Video #%d : %s' % (self.pk, self.title)

    class Meta:
        verbose_name = ugettext(u"Video")
