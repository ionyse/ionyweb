# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from ionyweb.plugin.models import AbstractPlugin


class Plugin_FbLikebox(AbstractPlugin):
    
    # Define your fields here
    href = models.URLField(_(u"Facebook profile's url"))
    width = models.PositiveIntegerField(_(u"width"),
                                        blank=True,
                                        null=True,
                                        help_text=_(u"You can set the likebox width in pixels.<br/>"
                                                    u"By default, the likebox will be 312px. "
                                                    u"Min width : 292px."))
    height = models.PositiveIntegerField(_(u"height"),
                                         blank=True,
                                         null=True,
                                         help_text=_(u"You can set the likebox height in pixels.<br/>"
                                                     u"By default, the height will be 260px"))
    colorscheme=models.CharField(_(u"Color's scheme"),
                                 max_length=10,
                                 choices=(('light', _(u'Light')),
                                          ('dark', _(u'Dark'))))
    show_faces = models.BooleanField(_(u'show faces?'))
    stream = models.BooleanField(_(u'stream?'))
    header = models.BooleanField(_(u'header?'))
    
    def __unicode__(self):
        return u'Facebook Likebox #%d : %s' % (self.pk, self.href)

    class Meta:
        verbose_name = _(u"Facebook Likebox")
