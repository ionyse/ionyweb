# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from ionyweb.page.models import AbstractPageApp

class PageApp_Text(AbstractPageApp):
    
    text = models.TextField(_(u"content's text"), blank=True)

    class Meta:
        verbose_name = _("Text App")

    def __unicode__(self):
        if self.text:
            if len(self.text) > 50:
                return u"%s..." % self.text[:47]
            else:
                return self.text
        else:
            return u"App Text #%d" % self.pk
