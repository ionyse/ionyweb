# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from ionyweb.plugin.models import AbstractPlugin


class Plugin_LinksList(AbstractPlugin):
    
    styled = models.BooleanField(_(u'show list decoration'),
                                 default=True)

    @property
    def links_list(self):
        return self.links.all().order_by('order')
    
    def nb_links(self):
        return self.links_list.count()
    nb_links.short_description = _(u"Links number")

    def __unicode__(self):
        return u'LinksList #%d : %s' % (self.pk, self.title)


    def deepcopy(self, **datas):
        # We make a copy of the plugin
        new_plugin = super(Plugin_LinksList, self).deepcopy(**datas)
        # We create new links objects
        for link in self.links.all():
            new_link = Link()
            new_link.text = link.text
            new_link.target = link.target
            new_link.order = link.order
            new_link.plugin = new_plugin
            new_link.save()
        return new_plugin

    class Meta:
        verbose_name = ugettext(u"Links List")
        verbose_name_plural = ugettext(u"Links Lists")

    class ActionsAdmin:
        actions_list = (
            {'title':_(u'Edit links'),
             'callback': "admin.plugin_links_list.edit_links"},
            )



class Link(models.Model):
    
    plugin = models.ForeignKey(Plugin_LinksList,
                               related_name='links')

    text = models.CharField(_(u"text"),
                            max_length=100)
    
    target = models.CharField(_(u"target"),
                              max_length=200)
    
    order = models.IntegerField(_(u"order"),
                                default=1)

    def save(self, *args, **kwargs):

        if not self.pk:
            try:
                # Get the last link order of the list
                last_link = list(self.plugin.links_list)[-1]
                self.order = last_link.order + 1
            except IndexError:
                self.order = 1
        
        return super(Link, self).save(*args, **kwargs)


    def __unicode__(self):
        return "%s : %s" % (self.text, self.target)


    class Meta:
        verbose_name = ugettext(u"Link")
        verbose_name_plural = ugettext(u"Links")
