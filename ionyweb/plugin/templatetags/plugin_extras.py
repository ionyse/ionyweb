# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='placeholder')
def placeholder(value, arg):
    """Filtre qui renvoie la liste de tous les plugins
    contenu dans le placeholder 'arg'.
    Les placeholders retournés sont supprimés de la liste
    'value'.
    """

    if value is None:
        return []

    item_returned = []
    indices_to_del = []

    # If default plugin, the entire value is returned
    # Be careful : the 'value' variable is not delete..
    if arg == settings.PLACEHOLDER_DEFAULT_ID :
        # if settings.DEBUG:
        #     print "=> ALL ITEMS ARE RETURNED"
        return value

    # General case :
    # Items in placeholder is returned and deleted from 'value' variable
    for i in xrange(len(value)):
        # If plugin is in this placeholder
        if value[i]['placeholder_slug'] == arg:
            # Plugin is copied to the returned list
            item_returned.append(value[i])
            # Indice is added to the del list
            # Be careful : it is necessary to add indices at the
            # front of the list otherwise deleting is compromised.
            indices_to_del.insert(0, i)
            
    # Del items of value
    for i in indices_to_del:
        del(value[i])

    return item_returned
