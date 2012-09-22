# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from ionyweb.plugin.models import AbstractPlugin


class Plugin_Map(AbstractPlugin):

    address = models.CharField(_(u'address'), max_length=200, blank=True, editable=False)
    map_lat = models.CharField(_(u'latitude'), max_length=25)
    map_lon = models.CharField(_(u'longitude'), max_length=25)

    description = models.TextField(_(u"description"), blank=True)

    window_open = models.BooleanField(_(u'Auto open the infobox'), default=False)

    zoom = models.IntegerField(_(u"zoom"), default=17)

    width = models.PositiveIntegerField(_(u"width"),
                                        blank=True,
                                        null=True)

    height = models.PositiveIntegerField(_(u"height"),
                                         blank=True,
                                         null=True)    

    def __unicode__(self):
        return u'Map (%s-%s) - %s' % (self.map_lat, 
                                       self.map_lon, 
                                       self.description)

    class Meta:
        verbose_name = ugettext(u"Map")

