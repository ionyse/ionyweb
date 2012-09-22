# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _
from django.conf import settings
# Visites 

# FIXME : Faire un model Traking qui sauvegarde les visites faites par
# un utilisateur sur les autres sites ionyweb en utilisant le login.js

class UserProfile(models.Model):
    
    ''' Special User for Ionyse '''
    user = models.ForeignKey(User, related_name="profile", unique=True)

    file_manager_display_mode = models.CharField(_(u"Display Mode"),
                                      max_length=1,
                                      choices=settings.DISPLAY_MODE,
                                      default="L",
                                      help_text=_(u"Display mode for directory content."))

def createUserProfile(sender, instance, **kwargs):
    """ Create a UserProfile object each time a User is created ; and
    link it.
    """
    UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(createUserProfile, sender=User)
