"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TransactionTestCase

from ionyweb.website.models import WebSite
from django.contrib.sites.models import Site
from ionyweb.file_manager.models import FileManager, Directory
from django.contrib.auth.models import User

import os


