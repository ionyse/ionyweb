# -*- coding: utf-8 -*-
import os
import sys

from django.utils.translation import ugettext as _

from django.conf import settings
from django.utils import simplejson

from ionyweb.loaders.storage import LayoutStorage, ThemeStorage

def list_layouts():
    ''' Return the list of availables layouts

    Available layouts are all layouts in dirs
    defined by settings.LAYOUT_DIRS.
    '''
    unique_slug = []
    layouts_list = []
    for layout_dir in settings.LAYOUTS_DIRS:
        layouts = LayoutStorage(location=layout_dir)
        directories, files = layouts.listdir('./')

        new_list = []
        for l in directories:
            if l not in unique_slug:
                new_list.append({'slug': l, 'path': layouts.path(l)} )
                unique_slug.append(l)
        layouts_list += new_list

    return layouts_list


def layouts_info():
    ''' Return list of informations about each available layout.

    Informations (title, slug, and preview) about each layout 
    are laoded from the `MANIFEST.json` file in layout dir (if it exists),
    else default informations are returned.
    '''

    layouts_list = []

    # Get all available layouts
    for layout in list_layouts():

        # Default infos
        current_layout = {'slug': layout['slug'],
                          'title': layout['slug'].capitalize(),
                          'preview': os.path.join(settings.STATIC_URL,
                                                  settings.LAYOUTS_DEFAULT_PATH,
                                                  'icon-layouts.png')}

        # Reading manifest file
        # and pickup infos (for updating default values)
        try:
            manifest_file = os.path.join(layout['path'], 'MANIFEST.json')
            with open(manifest_file, 'r') as f:
                try:
                    manifest = simplejson.loads(f.read())
                    if 'preview' in manifest.keys():
                        manifest['preview'] = '%slayouts/%s/%s' % (settings.STATIC_URL, 
                                                                   layout['slug'],
                                                                   manifest['preview'])
                except ValueError as e:
                    sys.stderr.write('JSON syntax error in %s\n%s\n\n' % (manifest_file, str(e)))
                    continue
                
                current_layout.update(**manifest)
        except IOError:
            pass
        layouts_list.append(current_layout)

    layouts_list = sorted(layouts_list, key=lambda layout: layout['title'].lower())
    return layouts_list



def list_themes():
    ''' Return the list of availables themes
    >>> list_themes()
    [{'path': u'~/hg/ionyweb3/ionyweb/contrib/themes/jungleland', 'slug': u'jungleland'}]

    '''

    unique_slug = []
    themes_list = []
    for theme_dir in settings.THEMES_DIRS:
        themes = ThemeStorage(location=theme_dir)
        directories, files = themes.listdir('./')

        new_list = []
        for t in directories:
            if t not in unique_slug:
                new_list.append({'slug': t, 'path': themes.path(t)})
                unique_slug.append(t)
        themes_list += new_list

    return themes_list


def get_theme(slug):
    
    theme = None
    for theme_dir in settings.THEMES_DIRS:
        themes = ThemeStorage(location=theme_dir)
        directories, files = themes.listdir('./')
        for t in directories:
            if t == slug:
                theme = {'slug': t, 'path': themes.path(t)}
                break
    return theme
    


def themes_info(slug=None):
    ''' Loads the MANIFEST for each available theme
    >>> themes_info()
    {u'natim': {'preview': '/_static/themes/icon-themes.png', 'title': u'natim'}, 
     u'jungleland': {'website': u'http://www.styleshout.com/', 'description': u'...', 
                     'title': u'Jungle Land', 'author': u'styleshout', 'date': u'01/09/2009', 
                     'preview': u'/_static/themes/jungleland/jungleland.jpg'}}
    '''
    # Get theme with slug or all themes list
    themes = []
    if slug is not None:
        theme_slug = get_theme(slug)
        if theme_slug:
            themes = [theme_slug]
        else:
            return None
    if not themes:
        themes = list_themes()

    themes_list = []
    for theme in themes:
        current_theme = {'slug': theme['slug'],
                         'title': theme['slug'].capitalize(),
                         'preview': ['%sthemes/icon-themes.png' % settings.STATIC_URL]}
        try:
            manifest_file = os.path.join(theme['path'], 'MANIFEST.json')
            with open(manifest_file, 'r') as f:
                try:
                    manifest = simplejson.loads(f.read())
                    # Set infos about preview files
                    if 'preview' in manifest.keys():
                        if isinstance(manifest['preview'], unicode) or isinstance(manifest['preview'], str):
                            previews = [manifest['preview']]
                        else:
                            previews = list(manifest['preview'])
                        manifest['preview'] = []
                        for preview in previews:
                            manifest['preview'].append(os.path.join(settings.STATIC_URL,
                                                                    settings.THEMES_DEFAULT_PATH,
                                                                    theme['slug'],
                                                                    preview))
                            
                    # set correct Path for each style        
                    if 'styles' in manifest.keys():  
                        for i in xrange(len(manifest['styles'])):
                            manifest['styles'][i]['preview'] = os.path.join(settings.STATIC_URL,
                                                               settings.THEMES_DEFAULT_PATH,
                                                               theme['slug'],
                                                               manifest['styles'][i]['preview'])
                        
                              
                    # Set infos about templates files
                    if 'templates' in manifest.keys():
                        templates_list = manifest['templates']
                        for template in templates_list:
                            template['preview'] = os.path.join(settings.STATIC_URL,
                                                               settings.THEMES_DEFAULT_PATH,
                                                               theme['slug'],
                                                               template['preview'])
                except ValueError as e:
                    sys.stderr.write('JSON syntax error in %s\n%s\n\n' % (manifest_file, str(e)))
                    continue

                current_theme.update(**manifest)
        except IOError:
            pass
        themes_list.append(current_theme)

    return themes_list
