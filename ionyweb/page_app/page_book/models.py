# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ionyweb.page.models import AbstractPageApp


class PageApp_Book(AbstractPageApp):
    title = models.CharField(_(u"title"), max_length=100)

    def _get_references(self):
        return self.references_set.all()

    references = property(_get_references)

    def __unicode__(self):
        return u'Book #%d : %s' % (self.pk, self.title)

    class Meta:
        verbose_name = _(u"Book App")

    class ActionsAdmin:
        actions_list = (
            {'title':_(u'Edit categories'), 'callback': "admin.page_book.edit_categories"},
            {'title':_(u'Edit clients'), 'callback': "admin.page_book.edit_clients"},
            {'title':_(u'Edit references'), 'callback': "admin.page_book.edit_references"},
            )


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Client(models.Model):
    name = models.CharField(_('name'), max_length=100)
    logo = models.CharField(_(u'logo'), help_text=_(u"client's logo"), max_length=200, blank=True)
    url = models.URLField(_(u'URL'))

    def __unicode__(self):
        return u"%s" % self.name

class Reference(models.Model):
    book = models.ForeignKey(PageApp_Book, related_name="references_set")

    title = models.CharField(_(u'title'),
                             max_length=50,
                             help_text = _(u'Reference\'s title'))
    description = models.CharField(_(u'description'),
                                   max_length=100,)    

    img = models.CharField(_(u'Screenshot'), max_length=100)
    url = models.URLField(_(u'URL'))
    date  = models.DateField(_(u'Realised at'),)

    client = models.ForeignKey(Client)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ['-date']
        verbose_name = _(u"Reference")

    def __unicode__(self):
        return u"%s - %s" % (self.client, self.title)
