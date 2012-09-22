#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

try:
    import django
    assert django.VERSION[0:2] == (1, 4)
except:
    print >> sys.stderr, "Don't forget to install Django-1.4\n    pip install Django"
    sys.exit(4)

try:
    import jinja2
except:
    print >> sys.stderr, "Don't forget to install python-jinja2\n    sudo apt-get install python-jinja2"
    sys.exit(4)

import os

from random import choice
from django.core import management
    
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('ionyweb.bin', 'templates/quickstart'))

def render_to_file(project_name, file_path, context={}):
    '''Render template with context and save to path.
    '''
    if file_path[0] == '.':
        template_name = file_path[1:]+'.tpl'
    else:
        template_name = file_path+'.tpl'

    template = env.get_template(template_name)
    data     = template.render(context)

    if not os.path.exists(project_name) and project_name != '':
        os.makedirs(os.path.join(project_name))

    out      = open(os.path.join(project_name, file_path), 'w+')
    out.write(data.encode('utf-8'))
    out.flush()
    out.close()

def write_file(project_name, file_path):
    '''Load the template and write it like this without jinja2 parsing
    '''
    if file_path[0] == '.':
        template_name = file_path[1:]+'.tpl'
    else:
        template_name = file_path+'.tpl'
    
    template = env.loader.get_source(env, template_name)
    data = template[0]

    if not os.path.exists(project_name) and project_name != '':
        os.makedirs(os.path.join(project_name))

    out = open(os.path.join(project_name, file_path), 'w+')
    out.write(data.encode('utf-8'))
    out.flush()
    out.close()
    

def start_project(project_name):
    if os.path.isfile(project_name):
        print >> sys.stderr, '%s already exists' % project_name
        return 2

    os.mkdir(project_name)

    open(os.path.join(project_name, '__init__.py'), 'w').close() 
    # create Makefile, settings.py and manage.py
    makefile = render_to_file(project_name, 'Makefile', {'PROJECT_NAME': project_name})
    settings = render_to_file(project_name,'settings.py', 
                              {'PROJECT_NAME': project_name, 
                               'SECRET_KEY': ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])})

    manage = render_to_file(project_name, 'manage.py', {'PROJECT_NAME': project_name})

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def usage():
    print u'USAGE : %s PROJECT_NAME' % sys.argv[0]

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) != 2:
        usage()
        return 1

    # Reading CLI args
    project_name = argv[1]

    return start_project(project_name)

if __name__ == "__main__":
    sys.exit(main())
