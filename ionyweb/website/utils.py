# -*- coding: utf-8 -*-
from hashlib import sha1

from django.conf import settings

def main_menus(request):
    if not getattr(request, 'page', None):
        return {}
    
    menus = request.website.pages.select_related()\
        .filter(is_diplayed_in_menu=True, 
                level__gte=0, 
                level__lte=getattr(request.website, 'main_menu_levels', 1)-1)\
        .order_by('tree_id', 'lft')

    if not request.is_admin:
        menus = menus.filter(draft=False)
        
    page = request.page

    return {'menu': menus,
            'page': page, 
            'website': request.website,
            'is_admin': request.is_admin}

def get_sha1_params_url(path_info):
    """Returns the sha1 of requested page and params app.

    """
    # if settings.DEBUG:
    #     print "## get_sha1_params_url() :"

    slug = ''
    params = ''
    params_admin = '/'
    index = 0
    separator = False
    error = False
    admin = False

    # We delete the first and last '/' for the next loop.
    items = path_info[1:]
    try:
        if items[-1] == u'/':
            items = items[:-1]
    except IndexError:
        pass

    items = items.split('/')

    # if settings.DEBUG:
    #     print "ITEMS : ", items


    # Detection of url params
    for item in items:
        if len(item) < settings.SLUG_MIN_SIZE:
            # Separator found => next items are the url app
            separator = items[index]
            break
        else:
            # This item still concerns the page slug, we continue the loop
            index += 1
    
    # We compute slug and params
    if separator:

        # Slug de la page
        slug = '/' + '/'.join(items[:index])

        # We check if there is a admin url
        # in the rest of the params
        if separator != settings.URL_ADMIN_SEP:
            try:
                wa_index = items[index+1:].index(settings.URL_ADMIN_SEP)
                # Update separator
                separator = settings.URL_ADMIN_SEP
                
                # if settings.DEBUG:
                #     print "Computing params_admin :"
                #     print "index : ", index
                #     print "wa_index : ", wa_index

                params = '/' + '/'.join(items[index+1:index+1+wa_index])
                params_admin = '/' + '/'.join(items[index+1:][wa_index+1:])
            except ValueError:
                params_admin = '/'
        else:
            params_admin = '/' + '/'.join(items[index+1:])
            params = '/'

        # If problems..
        if not params:
            params = '/' + '/'.join(items[index+1:])

        # if settings.DEBUG:
        #     print "## Separator found : ", separator

            
        # FIXME : Reorganize separator validity...

        # Check separator validity
        if separator == settings.URL_PAGE_APP_SEP:
            if params == '/':
                # url avec le tag de params, sans params
                error = True
        elif separator == settings.URL_ADMIN_SEP:
            # url de l'admin
            admin = True
            # Si params vide => ERROR
            if params_admin == '/':
                error = True
        else:
            # Separator non conforme
            error = True
    else:
        # if settings.DEBUG:
        #     print "## Separator not found"
        slug = path_info
        params = u'/'

    # Add the final '/' if missing
    if slug[-1] != u'/' :
        slug += u'/'
    if params[-1] != u'/' :
        params += u'/'
    if params_admin[-1] != u'/' :
        params_admin += u'/'

    # Computing sha1
    sha1_slug = sha1(slug).hexdigest()

    # if settings.DEBUG:
    #     print "slug : ", slug, " => ", sha1_slug
    #     print "params : ", params
    #     print "params admin : ", params_admin
    #     print "##"

    return {'sha1': sha1_slug,
            'params': params,
            'error': error,
            'admin': admin,
            'params_admin': params_admin}
