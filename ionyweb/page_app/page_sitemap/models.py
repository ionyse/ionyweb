# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ionyweb.page.models import AbstractPageApp


class PageApp_Sitemap(AbstractPageApp):
    
    def __unicode__(self):
        return u'Sitemap #%d' % (self.pk)

    class Meta:
        verbose_name = _(u"Sitemap App")
