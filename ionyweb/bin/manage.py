#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import argparse
from datetime import date

import shutil

try:
    from jinja2 import Environment, PackageLoader
except:
    print >> sys.stderr, "Don't forget to install Jinja2\n    pip install jinja2"
    sys.exit(4)

from ionyweb import get_ionyweb_path


RES_DIR = 'bin/templates'
PLUGINS_DIR = 'plugin_app'
APPS_DIR = 'page_app'
THEMES_DIR = 'themes'


def get_res_dir_path(dir_name=''):
    return os.path.join(get_ionyweb_path(), RES_DIR, dir_name)

def copy_file(template_filename, filename, plugin_path):
    shutil.copyfile(template_filename, os.path.join(plugin_path, filename))

def replace_to_file(template_filename, filename, plugin_path, context):
    if os.path.exists(plugin_path):
        data = open(template_filename, 'r').read()
        for rep in context.items():
            data.replace('{{ %s }}' % rep[0], rep[1])
            
        out = open(os.path.join(plugin_path, filename), 'w+')
        out.write(data.encode('utf-8'))
        out.flush()
        out.close()

def render_to_file(env, file_name, plugin_path, context={}):
    if os.path.exists(plugin_path):
        out = open(os.path.join(plugin_path, file_name), 'w+')
        template = env.get_template('%s.tpl' % file_name)
        data = template.render(context)            
        out.write(data.encode('utf-8'))
        out.flush()
        out.close()

def start_plugin(args):

    args.plugin_name.replace('plugin_', '')

    print "Starting creation of : %s\n" % args.plugin_name

    # Path of resource files dir for creating plugin
    plugin_res_dir = get_res_dir_path('plugin_templates')
    # Path of Plugins dir
    if os.path.exists(args.plugin_dir):
        plugins_dir = args.plugin_dir
    else:
        plugins_dir = args.plugin_dir
    # Complete path of plugin
    plugin_path = os.path.join(plugins_dir, 'plugin_%s' % args.plugin_name)
    # Plugin Object Name
    plugin_object_name = ''.join([item.capitalize() for item in args.plugin_name.split('_')])

    env = Environment(loader=PackageLoader('ionyweb.bin', 'templates/plugin_templates'))

    # Create plugin_app/plugin_name_dir
    if os.path.exists(plugin_path):
        print >> sys.stderr, 'Error : %s already exists' % plugin_path
        return 2
    os.mkdir(plugin_path)
    render_to_file(env, '__init__.py', plugin_path, context={'plugin_name': args.plugin_name})
    print 'Plugin dir created.'

    # Create models.py
    render_to_file(env, 'models.py', plugin_path, context={'plugin_object_name': plugin_object_name})
    print 'Plugin Models file created.'

    # Create views.py
    render_to_file(env, 'views.py', plugin_path, context={'plugin_name': args.plugin_name})
    print 'Plugin Views created.'

    # Create forms.py
    render_to_file(env, 'forms.py', plugin_path, context={'plugin_object_name': plugin_object_name})
    print 'Plugin Forms created.'

    # Create admin.py
    render_to_file(env, 'admin.py', plugin_path, context={'plugin_object_name': plugin_object_name})
    print 'Plugin Admin created.'

    # Create Templates Dir and index.html
    plugin_templates_dir = os.path.join(plugin_path, 'templates', 'plugin_%s' % args.plugin_name)
    os.makedirs(plugin_templates_dir)
    render_to_file(env, 'index.html', plugin_templates_dir, context={'plugin_object_name': plugin_object_name})
    print 'Plugin Templates created.'

    # Create Locale dir for traductions
    locale_dir = os.path.join(plugin_path, 'locale')
    os.mkdir(locale_dir)
    print 'Locale dir created.'

    print '\n\nNow just define your models,'
    print 'Custom the default template : \'index.html\','
    print 'Add your plugin to your INSTALLED_APPS : \'plugin_%s\'' % args.plugin_name
    print 'Synchronise the database.'
    print ' => Your plugin is fully configured !\n'


def start_app(args):
    args.app_name.replace('page_', '')

    print "Starting creation of : %s\n" % args.app_name

    # Path of resource files dir for creating app
    app_res_dir = get_res_dir_path('app_templates')
    # Path of Apps dir
    if os.path.exists(args.app_dir):
        apps_dir = args.app_dir
    else:
        apps_dir = os.path.join(get_ionyweb_path(), APPS_DIR)
    # Complete path of app
    app_path = os.path.join(apps_dir, 'page_%s' % args.app_name)
    # App Object Name
    app_object_name = ''.join([item.capitalize() for item in args.app_name.split('_')])

    env = Environment(loader=PackageLoader('ionyweb.bin', 'templates/app_templates'))

    # Create app_app/app_name_dir
    if os.path.exists(app_path):
        print >> sys.stderr, 'Error : %s already exists' % app_path
        return 2
    os.mkdir(app_path)
    open(os.path.join(app_path, '__init__.py'), 'w').close() 
    print 'App dir created.'

    # Create models.py
    render_to_file(env, 'models.py', app_path, context={'app_object_name': app_object_name})
    print 'App Models file created.'

    # Create views.py
    render_to_file(env, 'views.py', app_path, context={'app_name': args.app_name})
    print 'App Views created.'

    # Create forms.py
    render_to_file(env, 'forms.py', app_path, context={'app_object_name': app_object_name})
    print 'App Forms created.'

    # Create urls.py
    render_to_file(env, 'urls.py', app_path, context={'app_object_name': app_object_name})
    print 'App Urls created.'

    # Create admin.py
    render_to_file(env, 'admin.py', app_path, context={'app_object_name': app_object_name})
    print 'App Admin created.'

    # Create Templates Dir and index.html
    app_templates_dir = os.path.join(app_path, 'templates', 'page_%s' % args.app_name)
    os.makedirs(app_templates_dir)
    render_to_file(env, 'index.html', app_templates_dir, context={'app_object_name': app_object_name})
    print 'App Templates created.'

    # Create locale dir for translations
    locale_dir = os.path.join(app_path, 'locale')
    os.mkdir(locale_dir)
    print 'App Locale dir created.'

    print '\n\nNow just define your models,'
    print 'Custom the default template : \'index.html\','
    print 'Add your app to your INSTALLED_APPS : \'page_%s\'' % args.app_name
    print 'Synchronise the database.'
    print ' => Your app is fully configured !\n'

def start_theme(args):

    print "Starting creation of : %s\n" % args.theme_name
    theme_name = args.theme_name

    # Path of resource files dir for creating theme
    theme_res_dir = get_res_dir_path('themes_templates')
    # Path of Themes dir
    if not os.path.exists(args.theme_dir):
        os.makedirs(args.theme_dir)
    themes_dir = args.theme_dir
    # Complete path of theme
    theme_path = os.path.join(themes_dir, theme_name)

    env = Environment(loader=PackageLoader('ionyweb.bin', 'templates/theme_templates'))

    # Create theme_theme/theme_name_dir
    if os.path.exists(theme_path):
        print >> sys.stderr, 'Error : %s already exists' % theme_path
        return 2
    os.mkdir(theme_path)

    # Create MANIFEST.json
    render_to_file(env, 'MANIFEST.json', theme_path, 
                   context={'date': date.today().strftime('%d/%m/%Y'), 'theme_name': theme_name})
    print 'Theme MANIFEST.json file created.'

    # Create preview
    copy_file(os.path.join(get_res_dir_path('theme_templates'), 'preview.png'), 'preview.png', theme_path)
    print 'Theme preview.png created.'

    # Create favicon
    copy_file(os.path.join(get_res_dir_path('theme_templates'), 'favicon.ico'), 'favicon.ico', theme_path)
    print 'Theme favicon.ico created.'

    # Create Templates Dir and index.html
    theme_templates_dir = os.path.join(theme_path, 'templates')
    os.makedirs(theme_templates_dir)
    replace_to_file(os.path.join(get_res_dir_path('theme_templates'), 'index.html.tpl'), 
                    'index.html', theme_templates_dir, 
                   context={'theme_name': theme_name,
                            'theme_type': 'html5' })
    print 'Theme Templates created.'

    # Create css dir
    css_dir = os.path.join(theme_path, 'css')
    os.mkdir(css_dir)
    print 'Theme css dir created.'

    # Create style.css
    copy_file(os.path.join(get_res_dir_path('theme_templates'), 'styles.css'), 
              'styles.css', css_dir)
    print 'Initial styles.css created'

    print '\n\nNow just modify your template html and css,'
    print 'Do not forget to create a preview : \'preview.png\','
    print ' => Your theme is fully configured !\n'


def main():
    # Top level
    parser = argparse.ArgumentParser(prog='ionyweb-manage')
    subparsers = parser.add_subparsers()

    # Sub-command 'startplugin'
    parser_plugin = subparsers.add_parser('startplugin', help='startplugin help')
    parser_plugin.add_argument('plugin_name', type=str)
    default_plugins_dir = os.path.exists(PLUGINS_DIR) and PLUGINS_DIR or os.getcwd()
    parser_plugin.add_argument('--plugin_dir', type=str, nargs='?', default=default_plugins_dir)
    parser_plugin.set_defaults(func=start_plugin)

    # Sub-command 'startapp'
    parser_app = subparsers.add_parser('startapp', help='startapp help')
    parser_app.add_argument('app_name', type=str)
    default_apps_dir = os.path.exists(APPS_DIR) and APPS_DIR or os.getcwd()
    parser_app.add_argument('--app_dir', type=str, nargs='?', default=default_apps_dir)
    parser_app.set_defaults(func=start_app)

    # Sub-command 'starttheme'
    parser_theme = subparsers.add_parser('starttheme', help='starttheme help')
    parser_theme.add_argument('theme_name', type=str)
    default_themes_dir = os.path.exists(THEMES_DIR) and THEMES_DIR or os.getcwd()
    parser_theme.add_argument('--theme_dir', type=str, nargs='?', default=default_themes_dir)
    parser_theme.set_defaults(func=start_theme)

    # Parsing and call func
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
