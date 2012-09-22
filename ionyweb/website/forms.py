# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import Site
from ionyweb.forms import ModuloModelForm
import floppyforms as forms
from django.utils.translation import ugettext as _
from models import WebSite

# import floppyforms as forms

class Website_AnalyticsForm(ModuloModelForm):
    
    class Meta:
        model = WebSite
        fields = ['analytics_key']

#
class Website_ReferencementForm(ModuloModelForm):
    
    class Meta:
        model = WebSite
        fields = ['title', 'meta_keywords', 'meta_description']

class DomainWAForm(ModuloModelForm):

    def clean_domain(self):
        domain = self.cleaned_data.get('domain')

        # Test if the domain is restricted
        for rd in settings.RESTRICTED_DOMAINS:
            restricted_domain = '.%s' % rd
            if domain.endswith(restricted_domain):
                raise forms.ValidationError(
                    _(u"You cannot add a sub domain of this domain : `%(domain)s`") % 
                    {'domain': rd})

        # Test if the domain doesn't exists
        query = Site.objects.filter(domain=domain)
        if self.instance.pk is not None:
            query = query.exclude(pk=self.instance.pk)

        if query.count() > 0:
            raise forms.ValidationError(
                    _(u"The domain `%(domain)s` is already used by another site.") % 
                    {'domain': domain})                

        return domain
    
    class Meta:
        model = Site
        fields = ['domain']
