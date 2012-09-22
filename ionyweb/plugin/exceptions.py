# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

class PluginError(Exception):
    """Base class for exceptions in the plugin module."""
    
    def __init__(self, plugin=None, msg=None):
        if plugin:
            self.plugin_name = plugin.__class__.get_name_plugin()
        else:
            self.plugin_name = _(u'Plugin')

        if msg:
            self.msg = msg
        else:
            self.msg = _(u"An error has occured.")

    def __unicode__(self):
        return u'%s : %s' % (self.plugin_name, self.msg)


class PluginViewsNotProperlyConfiguredError(PluginError):
    """Default view exception.
    
    Occurs when the view `index_view()` is missing and
    the default `models.render_html()` method does not override.
    """

    def __init__(self, plugin=None):
        PluginError.__init__(self,
                             plugin,
                             msg=_(u'Define the `views.index_view()` function or '\
                                 u'overide the default `models.render_html()` method.'))



class PluginAdminNotProperlyConfiguredError(PluginError):
    """Default view exception.
    
    Occurs when the default admin form is missing.
    """

    def __init__(self, plugin=None):
        PluginError.__init__(self,
                             plugin,
                             msg=_(u'`models.get_admin_form()` method was not override.'))
