# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from ionyweb.plugin.models import AbstractPlugin

from views import index_view

class Plugin_Text(AbstractPlugin):

    text = models.TextField(_(u"text"))
    
    def __unicode__(self):
        return u'Text #%d : %s' % (self.pk, self.text[:50])
        
        
    class Meta:
        verbose_name = ugettext(u"Text")
