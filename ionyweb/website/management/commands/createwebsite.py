# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from ionyweb.website import create_new_website

class Command(BaseCommand):
    args = ''
    help = 'Create an empty but fonctionnal website'

    def handle(self, *args, **options):
        create_new_website()
