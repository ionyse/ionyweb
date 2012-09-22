# -*- coding: utf-8 -*-
" WebSite models "
import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import connection
from django.db import models
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template

from ionyweb.file_manager.models import FileManager, Directory


# Sites

class WebSite(models.Model):
    ''' WebSite
    New contract of WebSite.
    Everything is linked to an instance of this model.
    (Pages, Files, ...)
    '''
    slug = models.SlugField(_(u"url"),
                            max_length=100,
                            unique=True)

    title = models.CharField(_(u"title"),
                             max_length=50)

    logo = models.ImageField(_(u"Logo"),
                             upload_to='media_root',
                             # TEMP -> pbs with PIL...
                             blank=True)

    ndds = models.ManyToManyField(Site,
                                  related_name="website")

    owners = models.ManyToManyField(User,
                                    through='WebSiteOwner')

    domain = models.ForeignKey(Site,
                               related_name="website_set",
                               unique=True,
                               on_delete=models.PROTECT,
                               help_text=_(u"Represents the main domain of the "
                                           "website."))

    analytics_key = models.CharField(_("Analytics key"), max_length=20, blank=True, null=True, 
                                      #regex=r'UA-[0-9]{7}-[0-9]{1}',
                                      help_text=u'e.g. "UA-2456069-3"')

    main_menu_levels = models.PositiveIntegerField(_("Main menu levels"), default=1)

    meta_keywords = models.CharField(_(u"META Keywords"),
                                     max_length="255", blank=True)
    meta_description = models.TextField(_(u"META Description"), blank=True)


    theme = models.CharField(_(u'Theme slug'),
                             max_length=100)
    
    default_template = models.CharField(_(u'Default template'),
                                      max_length=100, blank=True)
    
    default_layout = models.CharField(_(u'Default layout'),
                                      max_length=100)
    # Warning, please use directory() to access the Files Library object
    files_library = models.ForeignKey(FileManager,
                                      related_name="website",
                                      blank=True,
                                      null=True,
                                      help_text=_(u"Files Library"))

    in_maintenance = models.BooleanField(_(u'Maintenance mode'), default=False, blank=True)

    class Meta:
        verbose_name = _(u"website")
        verbose_name_plural = _(u'websites')

    def __unicode__(self):
        return u'%s' % self.title
    
    def delete(self, *args, **kwargs):
        """ Delete this domain names linked to it and the files """
        for ndd in self.ndds.all():
            if ndd != self.domain:
                ndd.delete()
        save_ndd = self.domain
        #shutil.rmtree(self.media_root())
        super(WebSite, self).delete(*args, **kwargs)
        # The domain name is protected until the website is deleted successfully
        save_ndd.delete()
      
      
    def get_theme(self):
        if len(self.theme.split('/')) <= 1:
            return  "%s/default" % self.theme
        return self.theme
      
    def file_manager(self):
        if self.files_library:
            return self.files_library
        else:
            # Create root directory
            root = Directory.objects.create(name=self.slug)
            self.files_library = FileManager.objects.create(root=root)
            self.save()
            try:
                os.makedirs(self.media_root())
            except OSError:
                pass
            # Create
            try:
                os.makedirs(os.path.join(self.media_root(), 'storage'))
            except OSError:
                pass
            return self.files_library
        
    def media_root(self):
        "Get the filemanager site root"
        return os.path.join('websites', self.slug, 'storage')
    
    def get_size(self):
        "Give the size used for quota in bytes"
        return folder_size(self.media_root())

    def get_screenshot(self):
        "Return the url of the screenshot or None for the default image"
        return None

    def get_absolute_url(self):
        if getattr(settings, 'SERVER_PORT', 80) != 80:
            return u'http://%s:%d' % (self.domain.domain,
                                      settings.SERVER_PORT)
        else:
            return u'http://%s' % self.domain.domain
        
    def get_medias(self):
        # medias_list = []
        # # Add css file of the template
        # medias_list.append(
        #     u'<link href="http://%s%s" type="text/css" media="all" rel="stylesheet" />' % (
        #         self.domain.domain, self.skin.template.css_file ))
        # # Add css file of the skin
        # medias_list.append(
        #     u'<link href="http://%s%s" type="text/css" media="all" rel="stylesheet" />' % (
        #         self.domain.domain, self.skin.css_file ))
        # return u"\n".join(medias_list)
        return ""
    medias = property(get_medias)

    def _get_layout(self, layout_name=None):
        if layout_name is not None:
            return 'layouts/%s' % layout_name
        else:
            return ''

    def get_default_layout(self):
        return self._get_layout(self.default_layout)
    layout = property(get_default_layout)

    # def get_header_layout(self):
    #     return self._get_layout(self.header_layout)

    # def get_footer_layout(self):
    #     return self._get_layout(self.footer_layout)

    # def render_header(self, request):
    #     """
    #     Returns the header rendering of website.
    #     """
    #     return render_plugins_header_or_footer(
    #         request,
    #         plugins_list=self.header_plugins.order_by('plugin_order'),
    #         layout=self.get_header_layout())

    # def render_footer(self, request):
    #     """
    #     Returns the footer rendering of website.
    #     """

    #     return render_plugins_header_or_footer(
    #         request,
    #         plugins_list=self.footer_plugins.order_by('plugin_order'),
    #         layout=self.get_footer_layout())
    
    def get_url_home_page(self):
        return u'/'

class WebSiteOwner(models.Model):
    website = models.ForeignKey(WebSite, related_name='websites_owned')
    user = models.ForeignKey(User, related_name='websites_owned')
    is_superuser = models.BooleanField(_('superuser status'),
                                       default=False, 
                                       help_text=_("Designates that this user "
                                                  "has all permissions without "
                                                  "explicitly assigning them."))

    def __unicode__(self):
        return u'%s owns %d (%s)' % (self.user, self.website.id, self.is_superuser)

    def delete(self, *args, **kwargs):
        number_of_owners = self.website.websites_owned.filter(is_superuser=True).count()
        if number_of_owners <= 1 and self.is_superuser:
            raise IntegrityError('This user is the only superuser of this website')
        else:
            super(WebSiteOwner, self).delete(*args, **kwargs)

# SIGNALS
def catch_wrong_deletion_of_user(sender, instance, **kwargs):
    ''' Verify that if we delete the website owner, it will still have
    no orphans websites
    '''
    cursor = connection.cursor()
    cursor.execute("""
        SELECT ws.title, COUNT(*) as owners FROM `website_website` ws
        INNER JOIN website_websiteowner wso 
              ON ws.id = wso.website_id 
              AND wso.is_superuser = 1
              AND ws.id IN (SELECT website_id 
                            FROM website_websiteowner
                            WHERE user_id = %s)
        """, [instance.id])

    websites_owned = cursor.fetchall()

    websites_alone = []

    for website_title, owner_count in websites_owned:
        if website_title is not None and owner_count <= 1:
            websites_alone.append(website_title)

    if len(websites_alone) > 0:
        raise IntegrityError(
            'This user is the only owner of the website(s) : %s' % (
                ', '.join(websites_alone)))

models.signals.pre_delete.connect(catch_wrong_deletion_of_user, sender=User)

def create_filemanager_media_site_root(sender, instance, **kwargs):
    """Create the filemanager when creating a WebSite"""

    try:
        os.mkdir(instance.media_root())
        return True
    except OSError:
        return False

models.signals.post_save.connect(create_filemanager_media_site_root, sender=WebSite)

