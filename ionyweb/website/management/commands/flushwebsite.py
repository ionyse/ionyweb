# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from ionyweb.website import flush_website

class Command(BaseCommand):
    args = ''
    help = 'Flush all the database'

    def handle(self, *args, **options):
        flush_website()
