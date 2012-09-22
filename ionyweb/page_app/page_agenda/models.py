# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ionyweb.page.models import AbstractPageApp
import datetime
from django.utils.html import strip_tags

class PageApp_Agenda(AbstractPageApp):
    
    # Define your fields here
    title = models.CharField(_(u"title"), max_length=100)

    def __unicode__(self):
        return u'Agenda #%d' % (self.pk)

    @property
    def get_events(self):
        return self.get_events_for_date()

    def get_events_for_date(self, year=None, month=None, day=None):
        if (month is None) or (year is None):
            today = datetime.date.today()
            month = today.month
            year = today.year

        events = self.events.filter(start_date__year=year)\
                            .filter(start_date__month=month)\
                            .filter(is_published=True)

        if day is not None:
            events = events.filter(start_date__day=day)

        return events.order_by('start_date')

    class Meta:
        verbose_name = _(u"Agenda")

    class ActionsAdmin:
        title = _(u"Agenda")
        actions_list = (
            {'title':_(u'Edit events'), 
             'callback': "admin.page_agenda.edit_events"},
            )


class Event(models.Model):
    """
    Define an Event
    """

    app = models.ForeignKey(PageApp_Agenda,
                            related_name=u'events')

    title = models.CharField(_(u"Title"),
                             max_length=100,)

    description = models.TextField(_(u"Description"),
                                   blank=True)

    image = models.CharField(_(u'Image'),
                             max_length=100,
                             blank=True)

    place = models.CharField(_(u"Place"),
                             max_length=100,
                             blank=True)

    address = models.TextField(_(u"Address"),
                               blank=True)

    zipcode = models.CharField(_(u"zip code"),
                               max_length=10,
                               blank=True)

    city = models.CharField(_(u"city"),
                            max_length=100,
                            blank=True)

    start_date = models.DateTimeField(_(u"start date"))

    end_date = models.DateTimeField(_(u"end date"),
                                    blank=True,
                                    null=True)

    is_published = models.BooleanField(_(u"Is published"),
                                       default=True)

    last_modif = models.DateTimeField(_(u"Last modification"),
                                      editable=False,
                                      auto_now = True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name = _(u"Évènement")


    def clean(self):
        from django.core.exceptions import ValidationError
        # Vérification des concordances de dates
        if self.end_date is not None:
            if not self.end_date > self.start_date:
                raise ValidationError(_(u"You cannot end the event before it starts."))


    def _get_param_url(self):
        """
        Retourne les paramètres GET de l'url correspondant
        à cet évènement.
        """
        return u'?mois=%d&annee=%d' % (self.start_date.month, self.start_date.year)

    def get_absolute_url(self):
        return u'%s%s' % (self.app.get_absolute_url(), self._get_param_url())

    def __unicode__(self):
        return u"%s - %s..." % (self.start_date, self.description[:15])

    def display_description_admin(self):
        if self.description:
            value = strip_tags(self.description)
            if len(value)>50:
                value = value[:50] + u'...'
            return value
        else:
            return u''
    display_description_admin.short_description = _(u'Description')
    display_description_admin.admin_order_field = 'description'
    display_description_admin.allow_tags = True
