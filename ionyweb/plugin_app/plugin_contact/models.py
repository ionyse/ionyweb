# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from ionyweb.plugin.models import AbstractPlugin



class Plugin_Contact(AbstractPlugin):
    
    default_subject = models.CharField(_(u'Object'),
                                       max_length=50,
                                       blank=True,
                                       help_text=_(u"Enter a default object for this form. "
                                                   u"If set it will prefix the subject of the email sent."))

    email = models.EmailField(_(u'email'))

    def __unicode__(self):
        return u'Contact Form #%d : %s' % (self.pk, self.title)


    def get_admin_form(self):
        from forms import Plugin_ContactFormAdmin
        return Plugin_ContactFormAdmin

    @property
    def emails(self):
        return [self.email,]

    @property
    def subject(self):
        return self.default_subject

    class Meta:
        verbose_name = ugettext(u"Contact Form")
