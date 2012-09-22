# -*- coding: utf-8 -*-
from django.conf import settings

from django.utils.translation import ugettext as _
from djangorestframework.response import ErrorResponse
from djangorestframework import status

MESSAGES = {
    # General messages
    'default_error'        : _(u"Sorry, an error occured."),
    'item_edit_success'    : _(u"Element successfuly edited."),
    'item_creation_success': _(u"Element successfuly created."),
    'item_delete_success'  : _(u"Element successfuly deleted."),
    'items_edit_success'   : _(u"Elements successfuly edited."),
    'invalid_data'         : _(u"Some datas are not valid."),
    'plugin_delete_success': _(u"Plugin successfuly deleted."),
    'items_move_success'   : _(u"Items positions successly updated."),
    # Actions
    'action_not_found'     : _(u"Action not found."),
    # Apps
    'app_edit_success'     : _(u"Application successfuly edited."),
    # Login
    'user_already_auth'    : _(u"User already authenticated."),
    'user_authenticated'   : _(u"User authenticated."),
    'bad_login_pwd'        : _(u"Wrong login or password."),
    'inactive_user'        : _(u"Please activate your account."),
    # Layouts
    'layout_edit_succes'   : _(u"Layout successfuly updated."),
    # Themes
    'theme_edit_succes'    : _(u"Theme successfuly updated. Page is going to reload in few seconds."),
    # Pages
    'delete_home_page_error': _(u"You can't delete the home page."),
    'page_delete_success'   : _(u"Page successfuly deleted."),
    'page_draft_toggle'    : _(u"Page's draft status toggled."),
    # File Manager
    'no_file'    : _(u"Must have files attached!"),
}


def check_object_html_id(html_id, types=[settings.SLUG_PLUGIN]):
    """
    Check if the plugin html ID is valid and
    return its ID.
    Valid IDs examples are : 'plugin-relation-1' or 'app-12' if in types

    Parameters :
      - types       : list of types id that we have to accept
    
    If ID doesn't valid, raise a response 400.
    """
    items = html_id.rsplit(settings.SLUG_SEP, 1)

    if len(items) != 2 or items[0] not in types:
        raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                            {'msg': MESSAGES.get('default_error', "")})
    return items


def check_placeholder_html_id(html_id, extras_id=[]):
    """
    Check if the placeholder html ID is valid and return split of ID.
    Valid IDs examples are : 'header-placeholder-1' or
    'clipboard-placeholder'.
    
    If ID doesn't valid, raise a response 400.

    Parameters :
      - extras_id   : List of additional id value.
                      If list is empty, just int value is accepted.
    """
    # Extra ID accepted, eg placeholder default.
    if html_id in extras_id:
        return html_id

    # Check structure of html id
    items_html_id = html_id.rsplit(settings.SLUG_SEP, 2)
    if len(items_html_id) != 3 or\
            items_html_id[1] != settings.SLUG_PLACEHOLDER:
        raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                            {'msg': MESSAGES.get('default_error', "")})
    # Last item must be an int
    try:
        int(items_html_id[2])
    except ValueError:
        raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                            {'msg': MESSAGES.get('default_error', "")})
    return items_html_id

def is_page_placeholder_html_id(html_id):
    """
    Check if the placeholder_html_id contains page plugins or website plugins
    """
    return html_id.startswith(settings.SLUG_CONTENT)
