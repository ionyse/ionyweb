# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from ionyweb.forms import ModuloModelForm, IonywebContentForm

import floppyforms as forms

from models import Plugin_Contact


class Plugin_ContactForm(IonywebContentForm, forms.Form):
    """
    Contact form use to display the plugin
    """

    name = forms.CharField(label=_(u'Name :'), required=False)
    mail = forms.EmailField(label=_(u'Email *:'))
    subject = forms.CharField(label=_(u'Object :'), required=False)
    message = forms.CharField(label=_(u"Message *:"), widget=forms.Textarea)

    def send(self, mails=[], default_subject=""):

        if self.is_valid():
            if not mails:
                mails = [a[1] for a in settings.ADMINS]

            if default_subject:
                default_subject = u'[' + default_subject + ']'

            subject = u'[%s]%s %s' % (settings.SITE_NAME,
                                        default_subject,
                                        self.cleaned_data['subject'])

            msg = EmailMessage(subject, self.cleaned_data['message'],
                               self.cleaned_data['mail'], mails)
            try:
                msg.send()
            except:
                return False

            return True

        return False

class Plugin_ContactFormAdmin(ModuloModelForm):
    """
    Plugin form to edit the plugin
    """

    class Meta:
        model = Plugin_Contact
