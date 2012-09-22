# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ionyweb.plugin.models import AbstractPlugin


class Plugin_Breadcrumb(AbstractPlugin):
    
    separator = models.CharField(_(u'separator'), max_length=10, blank=True,
                                 help_text=_(u'Define a separator string.'))

    ancestors_displayed = models.BooleanField(_(u'ancestors displayed?'), default=True,
                                              help_text=_(u"Activate this option for display all ancestors pages in breadcrumb."))
    
    links_enabled = models.BooleanField(_(u'Links enabled?'), default=True,
                                       help_text=_(u"Enable/Disable link on each item."))
                                              

    def __unicode__(self):
        return u'Breadcrumb #%d' % (self.pk)

    def get_separator(self):
        if self.separator:
            return self.separator
        return u'/'

    class Meta:
        verbose_name = _(u"Breadcrumb")
        verbose_name_plural = _(u"Breadcrumbs")
