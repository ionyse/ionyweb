# -*- coding: utf-8 -*-

import floppyforms as forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from django.conf import settings

from ionyweb.forms import ModuloModelForm
from ionyweb.page.models import Page
from ionyweb.page.utils import errors_append
from ionyweb.settings import SLUG_MIN_SIZE
from ionyweb.widgets import SlugWidget, TemplateThemeSelectWidget
from ionyweb.loaders.manifest import themes_info


def content_type_choices(limit_choices_to={}):
    content_types = []
    for content_type in ContentType.objects.filter(**limit_choices_to):
        content_types.append((content_type.pk, content_type.model_class()._meta.verbose_name))

    return content_types

LIMIT_CHOICES_TO = {'model__startswith': 'pageapp_'}

class PageWAForm(ModuloModelForm):
    app_page_type = forms.ModelChoiceField(queryset=ContentType.objects.filter(**LIMIT_CHOICES_TO), 
                                           empty_label=None)
    default_template = forms.ChoiceField(label=_(u'template'),
                                         help_text=_(u'Select the theme template for the page.'),
                                         widget=TemplateThemeSelectWidget, required=False)

    def __init__(self, *args, **kwargs):
        super(PageWAForm, self).__init__(*args, **kwargs)
        self.fields['app_page_type'].choices = content_type_choices(LIMIT_CHOICES_TO)
        # Need to hide 'default_template' by default
        hide_default_tpl_field = True
        # Only if edition mode
        if hasattr(self.instance, 'pk'):
            if self.instance.pk:
                # Add help_text
                self.fields['app_page_type'].help_text = _(u"Be careful : if you change the app type, "
                                                           u"the current app will be deleted.")
                # Hide the slug field if we edit the homepage
                if self.instance.is_homepage:
                    self.fields['slug'].widget = forms.HiddenInput()

                # Initialization of templates theme
                theme_infos = themes_info(self.instance.website.theme.split('/')[0])[0]
                if 'templates' in theme_infos:
                    # Theme has many templates
                    # we set the choices with those values
                    choices_default_templates = []
                    for template in theme_infos['templates']:
                        if template['file'] == settings.TEMPLATE_THEME_FILE_DEFAULT:
                            file_value = ""
                        else:
                            file_value = template['file']
                        choices_default_templates.append((
                                file_value,
                                ({'title': template['title'], 'preview': template['preview']}),
                                ))
                    self.fields['default_template'].choices = choices_default_templates
                    # We don't hide the field
                    hide_default_tpl_field = False

        if hide_default_tpl_field:
            # The theme defines only one template,
            # so we hide the field and we add the current value of template page
            # in choices to avoid error validation
            self.fields['default_template'].choices = [(self.instance.default_template, '')]
            self.fields['default_template'].widget = forms.HiddenInput()
            

        
    def clean(self):        
        # Get the website
        website = self.cleaned_data['website']

        if 'slug' in self.cleaned_data:
            slug = self.cleaned_data['slug']
        else:
            return self.cleaned_data

        # Get the previous data to see if it was modified
        if self.instance.id:
            page = Page.objects.get(id = self.instance.id)
            if page.slug == slug:
                return self.cleaned_data
            elif page.is_homepage:
                errors_append(self, 'slug', _(u'You cannot change the homepage slug.'))

        # The only empty slug page should be the home page.
        if slug == "" and self.cleaned_data.get('parent', None) is not None:
            errors_append(self, 'slug', _(u'A page without slug cannot have a parent'))
            return self.cleaned_data

        # Does this slug is already used ?
        if Page.objects.filter(slug__exact=slug, website__exact=website, parent=self.cleaned_data.get('parent', None)).count() != 0:
            errors_append(self, 'slug', _(u'This slug is already used by another page.'))
            return self.cleaned_data
        
        # Does the slug has the minimum size
        if len(slug) > 0 and len(slug) < SLUG_MIN_SIZE:
            errors_append(self, 'slug', _(u'A slug should be at least %(min_size)d characters long.') % {'min_size' : SLUG_MIN_SIZE})
            return self.cleaned_data

        # Parent should exist and should not be home
        if self.cleaned_data.get('parent', None) is not None:
            if self.cleaned_data['parent'].slug == "":
                errors_append(self, 'parent', _(u'You cannot add a sub_page to the empty slug page.'))
        return self.cleaned_data
        
    class Meta:
        model = Page
        fields = ('website',
                  'parent',
                  'title',
                  'slug',
                  'draft',
                  'app_page_type',
                  'is_diplayed_in_menu',
                  'menu_title',
                  'meta_keywords',
                  'meta_description',
                  'default_template')
        widgets = {
            'meta_description': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'website': forms.HiddenInput(),
            'slug': SlugWidget('title'),
            'parent': forms.HiddenInput(attrs={'value': ""}),
        }

    
