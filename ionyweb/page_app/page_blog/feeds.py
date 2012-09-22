# -*- coding: utf-8
"""
Feeds of ``blog`` application.
"""
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site

from ionyweb.page_app.page_blog.models import Category, Entry

class RssEntries(Feed):
    """
    RSS entries.
    """
    title_template = "page_blog/feeds/entry_title.html"
    description_template = "page_blog/feeds/entry_description.html"

    def get_object(self, request, obj, *args, **kwargs):
        return obj

    def title(self, obj):
        """
        Channel title.
        """
        return _('%(site_name)s: RSS entries') % {
            'site_name': obj.title,
        }

    def description(self, obj):
        """
        Channel description.
        """
        return _('RSS feed of recent entries posted on %(site_name)s.') % {
            'site_name': obj.title,
        }

    def link(self, obj):
        """
        Channel link.
        """
        return obj.get_absolute_url()

    def items(self, obj):
        """
        Channel items.
        """
        return obj.online_entries.order_by('-publication_date')[:10]

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        """
        Channel item publication date.
        """
        return item.publication_date

class RssCategory(RssEntries):
    """
    RSS category.
    """
    def title(self, obj):
        """
        Channel title.
        """
        return _('%(site_name)s: RSS %(category)s category') % {
            'site_name': obj.blog.title,
            'category': obj.name,
        }

    def description(self, obj):
        """
        Channel description.
        """
        return _('RSS feed of recent entries posted in the category %(category)s on %(site_name)s.') % {
            'category': obj.name,
            'site_name': obj.blog.title,
        }

    def link(self, obj):
        """
        Channel link.
        """
        return obj.get_absolute_url()

    def get_object(self, request, obj, *args, **kwargs):
        """
        Object: the Category.
        """
        return obj.online_categories.get(slug=kwargs['slug'])

    def items(self, obj):
        """
        Channel items.
        """
        return obj.online_entries

    def item_pubdate(self, item):
        """
        Channel item publication date.
        """
        return item.publication_date
