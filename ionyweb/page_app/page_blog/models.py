# -*- coding: utf-8 -*-
"""
Models of ``blog`` application.
"""
from datetime import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from mptt.models import MPTTModel, TreeForeignKey

from ionyweb.page.models import AbstractPageApp
from ionyweb.page_app.page_blog.managers import CategoryOnlineManager, EntryOnlineManager


class PageApp_Blog(AbstractPageApp):
    
    title = models.CharField(_(u"title"), max_length=100)

    class Meta:
        verbose_name_plural = verbose_name = _("Blog App")

    class ActionsAdmin:
        actions_list = (
            {'title':_(u'Edit categories'), 'callback': "admin.page_blog.edit_categories"},
            {'title':_(u'Edit entries'), 'callback': "admin.page_blog.edit_entries"},
            )

    def __unicode__(self):
        if self.title:
            if len(self.title) > 50:
                return u"%s..." % self.title[:47]
            else:
                return self.title
        else:
            return u"App Blog #%d" % self.pk

    def _get_online_entries(self):
        """
        Returns entries in this category with status of "online".
        Access this through the property ``online_entry_set``.
        """
        from models import Entry
        return self.entries.distinct().filter(status=Entry.STATUS_ONLINE)

    online_entries = property(_get_online_entries)

    def _get_online_categories(self):
        """
        Returns categories with entries "online" inside.
        Access this through the property ``online_entry_set``.
        """
        from models import Entry
        queryset =  self.categories.distinct().filter(entries__status=Entry.STATUS_ONLINE)

        new_queryset = queryset.distinct().none() | queryset
        for obj in queryset:
            new_queryset = new_queryset | obj.get_ancestors().distinct()

        return new_queryset
        
    online_categories = property(_get_online_categories)

    def get_absolute_url(self):
        return self.page.get().get_absolute_url()

    def get_sitemap(self):
        from sitemap import BlogSitemap
        return BlogSitemap(blog=self)

    def details(self):
        response = u""
        entries = self.entries.count()
        response += u"%d " % entries
        if entries <= 1:
            response += u"%s " % _(u'entry')
        else:
            response += u"%s " % _(u'entries')
        categories = self.categories.count()
        response += u" %s %d " % (_(u'and'), categories)
        if categories <= 1:
            response += u"%s " % _(u'category')
        else:
            response += u"%s " % _(u'categories')
            
        return response


class Category(MPTTModel):
    """
    A blog category.
    """
    blog = models.ForeignKey(PageApp_Blog, related_name="categories")
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('edit date'), auto_now=True)

    objects = models.Manager()
    online_objects = CategoryOnlineManager()

    class Meta:
        unique_together = (("blog", "slug"),)
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('tree_id', 'lft')

    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by=['slug']

    def __unicode__(self):
        return u'%s' % self.name

    def get_title(self):
        prefix = ''
        for i in xrange(self.level):
            prefix += '---'
        return u'%s %s' % (prefix, self.name)

    get_title.short_description = _('name')

    def get_absolute_url(self):
        return u"%s%s%s" % (self.blog.get_absolute_url(),
                            settings.URL_PAGE_APP_SEP,
                            reverse('blog_category', kwargs={'slug': self.slug,}, 
                                    urlconf='ionyweb.page_app.page_blog.urls'))

    def _get_online_entries(self):
        """
        Returns entries in this category with status of "online".
        Access this through the property ``online_entry_set``.
        """
        from models import Entry        
        return Entry.objects.distinct().filter(status=Entry.STATUS_ONLINE, 
                                               category__lft__gte=self.lft, 
                                               category__rght__lte=self.rght,
                                               category__tree_id=self.tree_id).order_by('category__tree_id', 'category__lft')

    online_entries = property(_get_online_entries)

class Entry(models.Model):
    """
    A blog entry.
    """
    STATUS_OFFLINE = 0
    STATUS_ONLINE = 1
    STATUS_DEFAULT = STATUS_OFFLINE
    STATUS_CHOICES = (
        (STATUS_OFFLINE, _('Offline')),
        (STATUS_ONLINE, _('Online')),
    )

    blog = models.ForeignKey(PageApp_Blog, related_name="entries")

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique_for_date='publication_date')
    author = models.ForeignKey('auth.User', verbose_name=_('author'))
    category = TreeForeignKey(Category, verbose_name=_('category'), related_name="entries")
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    publication_date = models.DateTimeField(_('publication date'), 
                                            default=datetime.now(),
                                            db_index=True)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_DEFAULT, db_index=True)
    body = models.TextField(_('body'))

    objects = models.Manager()
    online_objects = EntryOnlineManager()

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __unicode__(self):
        return u'%s' % self.title
    
    def get_title(self):
        return u'%s' % self.title
    get_title.action_short_description=_(u'Title')
    
    def get_category(self):
        return u'%s' % self.category
    get_category.action_short_description=_(u'Category')
    
    def get_publication_date(self):
        return u'%s' % self.publication_date
    get_publication_date.action_short_description=_(u'Publication Date')
    
    def get_status(self):
        return self.STATUS_CHOICES[self.status][1]
    get_status.action_short_description=_(u'Status')

    def get_absolute_url(self):
        return u"%s%s%s" % (self.blog.get_absolute_url(),
                            settings.URL_PAGE_APP_SEP,
                            reverse('blog_entry', kwargs={
                                      'year': self.publication_date.strftime('%Y'),
                                      'month': self.publication_date.strftime('%m'),
                                      'day': self.publication_date.strftime('%d'),
                                      'slug': self.slug,
                            }, urlconf='ionyweb.page_app.page_blog.urls'))
