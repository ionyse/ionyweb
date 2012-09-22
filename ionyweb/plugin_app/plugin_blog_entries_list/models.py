# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from ionyweb.plugin.models import AbstractPlugin
from ionyweb.page_app.page_blog.models import Entry


class Plugin_BlogEntriesList(AbstractPlugin):
    
    @property
    def entries_list(self):
        return self.entries.all().order_by('order')
    
    def nb_links(self):
        return self.entries_list.count()
    nb_links.short_description = _(u"Entries number")

    def __unicode__(self):
        return u'EntriesList #%d : %s' % (self.pk, self.title)


    def deepcopy(self, **datas):
        # We make a copy of the plugin
        new_plugin = super(Plugin_BlogEntriesList, self).deepcopy(**datas)
        # We create new links objects
        for link in self.entries.all():
            new_link = EntryLink()
            new_link.text = link.text
            new_link.entry = link.entry
            new_link.order = link.order
            new_link.plugin = new_plugin
            new_link.save()
        return new_plugin

    def __unicode__(self):
        return u'BlogEntriesList #%d' % (self.pk)

    class Meta:
        verbose_name = ugettext(u"Entries List")
        verbose_name_plural = ugettext(u"Entries Lists")
        
    class ActionsAdmin:
        actions_list = (
            {'title':_(u'Edit entries'), 'callback': "admin.plugin_blog_entries.edit_entries"},
            )

        

class EntryLink(models.Model):
    
    plugin = models.ForeignKey(Plugin_BlogEntriesList,
                               related_name='entries')

    text = models.CharField(_(u"text"),
                            max_length=100)
    
    entry = models.ForeignKey(Entry,
                               related_name='entries')
    
    order = models.IntegerField(_(u"order"),
                                default=1)

    def save(self, *args, **kwargs):

        if not self.pk:
            try:
                # Get the last link order of the list
                last_link = list(self.plugin.entries_list)[-1]
                self.order = last_link.order + 1
            except IndexError:
                self.order = 1
        
        return super(EntryLink, self).save(*args, **kwargs)


    def __unicode__(self):
        return "%s : %s" % (self.text, self.entry)


    class Meta:
        verbose_name = ugettext(u"Entry")
        verbose_name_plural = ugettext(u"Entries")
