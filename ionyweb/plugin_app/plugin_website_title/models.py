# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from ionyweb.plugin.models import AbstractPlugin


class Plugin_WebsiteTitle(AbstractPlugin):
    
    baseline = models.CharField(_(u'baseline'),
                                max_length=200,
                                blank=True,
                                help_text=_(u'Define a baseline for your website.'))

    link_enabled = models.BooleanField(_(u'enable link title'),
                                       default=True)

    target_link = models.CharField(_(u'link'), max_length=200,
                                   blank=True, default = '/')

    margin_top = models.CharField(_(u'margin top'), blank=True,
                                  max_length=10)
    margin_bottom = models.CharField(_('margin bottom'), blank=True,
                                     max_length=10)

    def link_url(self):
        if self.target_link:
            return self.target_link
        return u'/'

    def __unicode__(self):
        return u'Website Title #%d : %s' % (self.pk, self.title)

    class Meta:
        verbose_name = ugettext(u"Website Title")
