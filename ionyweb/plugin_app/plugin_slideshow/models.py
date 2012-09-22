# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from ionyweb.plugin.models import AbstractPlugin
from django.conf import settings


FX_VALUES = (
    ('FA', _(u'Fade'), 'fade'),
    ('SL', _(u'Scroll Left'), 'scrollLeft'),
    # ('SU', _(u'Scroll Up'), 'scrollUp'),
    # ('SD', _(u'Scroll Down'), 'scrollDown'),
    ('SR', _(u'Scroll Right'), 'scrollRight'),
    )


class Plugin_Slideshow(AbstractPlugin):
    
    FX_CHOICES = tuple([(code, verbose_name) for code, verbose_name, value in FX_VALUES])
    MAX_WIDTH_IMAGE = 1920
    MAX_HEIGHT_IMAGE = 1080
    PREFERRED_HEIGHT_IMAGE = 350

    fx = models.CharField(_(u"Effect"),
                          max_length=3,
                          choices=FX_CHOICES,
                          default='FA',
                          help_text=_(u"Select the transition effect."))
    
    speed = models.IntegerField(_(u"Speed transition"),
                                blank=True, null=True,
                                default=1000,
                                help_text=_(u"The speed option defines the number of "
                                            u"milliseconds it will take to transition "
                                            u"from one slide to the next."))

    timeout = models.IntegerField(_(u"Timeout transition"),
                                  blank=True, null=True,
                                  default=4000,
                                  help_text=_(u"The timeout option specifies how many "
                                              u"milliseconds will elapse between the start "
                                              u"of each transition."))

    pause = models.BooleanField(_(u"Pause"),
                                default=False,
                                help_text=_(u"The pause option causes the slideshow to pause "
                                            u"when the mouse hovers over the slide."))

    random = models.BooleanField(_(u"Random"),
                                 default=False,
                                 help_text=_(u"The random option causes the slides to be shown "
                                             u"in random order, rather than sequential."))

    pager = models.BooleanField(_(u"Pager"),
                                default=False,
                                help_text=_(u"The pager option allow to display a selector "
                                            u"item for the slideshow."))

    pager_thumbs = models.BooleanField(_(u"Pager thumbs"),
                                       default=False,
                                       help_text=_(u"The pager thumbs option allow to display "
                                                   u"thumbnails in the pager selector."))

    width_image = models.PositiveIntegerField(_(u"width"),
                                              blank=True,
                                              null=True,
                                              help_text=_(u"You can set the slideshow width in pixels. "
                                                          u"By default, the slideshow will take 100%% of "
                                                          u"length available. "
                                                          u"Max width : %(size)s px.") % {'size': MAX_WIDTH_IMAGE})

    height_image = models.PositiveIntegerField(_(u"height"),
                                               blank=True,
                                               null=True,
                                               help_text=_(u"You can set the slideshow height in pixels. "
                                                           u"The default height is %(size)s px.") % 
                                                           {'size': PREFERRED_HEIGHT_IMAGE})
    
    @property
    def width(self):
        if self.width_image:
            return min(self.width_image, self.MAX_WIDTH_IMAGE)
        return None

    @property
    def height(self):
        if self.height_image:
            return min(self.height_image, self.MAX_HEIGHT_IMAGE)
        return self.PREFERRED_HEIGHT_IMAGE

    @property
    def slides_list(self):
        return self.slides.order_by('order')

    def __unicode__(self):
        return u'Slideshow #%d' % (self.pk)

    def deepcopy(self, **datas):
        # We make a copy of the plugin
        new_plugin = super(Plugin_Slideshow, self).deepcopy(**datas)
        # We create new slides objects
        for slide in self.slides.all():
            new_slide = Slide()
            new_slide.image = slide.image
            new_slide.order = slide.order
            new_slide.plugin = new_plugin
            new_slide.save()
        return new_plugin

    class Meta:
        verbose_name = _(u"Slideshow")
        verbose_name_plural = _(u"Slideshows")

    class ActionsAdmin:
        actions_list = (
            {'title':_(u'Edit slides'), 'callback': "admin.plugin_slideshow.edit_slides"},
            )


class Slide(models.Model):

    plugin = models.ForeignKey(Plugin_Slideshow,
                               related_name='slides')

    image = models.CharField(_(u'Image'),
                             max_length=200)

    order = models.IntegerField(_(u'Order'),
                                default=1)

    def __unicode__(self):
        return u'Slide #%d' % (self.pk)

    def get_thumb(self):
        render = render_to_string('plugin_slideshow/action_admin_thumbnail.html',
                                {'path': self.image.path,
                                 'ADMIN_THUMBNAIL': settings.ADMIN_THUMBNAIL})
        return render
    get_thumb.action_short_description=_(u'Thumbnail')

    class Meta:
        verbose_name = _(u"Slide")
        verbose_name_plural = _(u"Slides")

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                # Get the last slide order of the list
                last_slide = list(self.plugin.slides_list)[-1]
                self.order = last_slide.order + 1
            except IndexError:
                self.order = 1
        return super(Slide, self).save(*args, **kwargs)
