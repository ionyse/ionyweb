# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

class PageAppError(Exception):
    """Base class for exceptions in the page app module."""
    
    def __init__(self, app=None, msg=None):
        if app:
            self.app_name = app.__class__.get_name()
        else:
            self.app_name = _(u'Page App')

        if msg:
            self.msg = msg
        else:
            self.msg = _(u"An error has occured.")

    def __unicode__(self):
        return u'%s : %s' % (self.app_name, self.msg)


class PageAppAdminNotProperlyConfiguredError(PageAppError):
    """Default view exception.
    
    Occurs when the default admin form is missing.
    """

    def __init__(self, app=None):
        PageAppError.__init__(self,
                             app,
                             msg=_(u'`models.get_admin_form()` method does not override.'))
