# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ionyweb.page.models import AbstractPageApp


class PageApp_{{ app_object_name }}(AbstractPageApp):
    
    # Define your fields here

    def __unicode__(self):
        return u'{{ app_object_name }} #%d' % (self.pk)

    class Meta:
        verbose_name = _(u"{{ app_object_name }}")
