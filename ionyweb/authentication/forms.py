# -*- coding: utf-8 -*-

import floppyforms as forms

from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
import dns.resolver

from ionyweb.authentication.models import UserProfile

class AutofocusInput(forms.TextInput):
    template_name = 'floppyforms/autofocus.html'

    def get_context_data(self):
        self.attrs['autofocus'] = True
        return super(AutofocusInput, self).get_context_data()


class EditCurrentUser(forms.Form):
    
    email = forms.EmailField(label = _(u"Email Address"),
                             help_text="",
                             required=True)
    
    def __init__(self, user, *args, **kwargs):
        super(EditCurrentUser, self).__init__(*args, **kwargs)
        self.fields['email'].initial = user.email


    def clean_email(self):
        "Check the email domain for MX DNS record"
        email = self.cleaned_data['email']

        user, domain = email.split('@')

        # Checking if the domain contains a MX record
        try:
            answers = dns.resolver.query(domain, 'MX')
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            raise forms.ValidationError(_(u"Emails from this domain are not "
                                          u"accepted"))
        else:
            return email
        
    
    def save(self, user, *args, **kwargs):
        user.email = self.cleaned_data['email']
        user.save()

        