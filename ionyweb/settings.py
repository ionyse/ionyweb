# -*- coding: utf-8 -*-
# Django settings for the jungleland project.
from ionyweb import get_ionyweb_path

import os

SITE_ID = 1
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTH_PROFILE_MODULE = 'authentication.UserProfile'

USE_I18N = True
USE_L10N = True

LOCALE_PATHS = (
    os.path.join(get_ionyweb_path(), 'locale'),
)

STATIC_URL = '/_static/'
MEDIA_URL = '/_medias/'

GRAPPELLI_ADMIN_URL = '/_admin/'
ADMIN_MEDIA_PREFIX = '/_static/grappelli/'

INTERNAL_IPS = ('127.0.0.1', )

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(get_ionyweb_path(), 'static'),
)

STATICFILES_FINDERS = (
    'ionyweb.loaders.layouts_finders.StaticFinder',
    'ionyweb.loaders.themes_finders.StaticFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'ionyweb.loaders.layouts_templates.Loader',
    'ionyweb.loaders.themes_templates.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',
    'sekizai.context_processors.sekizai',
    'ionyweb.context_processors.user_rights',
    'ionyweb.context_processors.admin_page_data',
    'ionyweb.context_processors.site_settings',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'ionyweb.website.middleware.ProvideWebSiteMiddleware',
    'ionyweb.website.middleware.PreamptiveWebSiteMiddleware',
)

ROOT_URLCONF = 'ionyweb.urls'
URLCONF_WEBSITE_ADMIN = u'ionyweb.administration.urls'

TEMPLATE_DIRS = (
    os.path.join(get_ionyweb_path(), 'templates'),
)

LAYOUTS_DEFAULT_PATH = 'layouts'
LAYOUTS_DIRS = (
    os.path.join(get_ionyweb_path(), 'contrib', LAYOUTS_DEFAULT_PATH),
)

THEMES_DEFAULT_PATH = 'themes'
THEMES_DIRS = (
    os.path.join(get_ionyweb_path(), 'contrib', THEMES_DEFAULT_PATH),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'tinymce',
    'mptt',
    'floppyforms',
    'south',
    'sekizai',
    'djangorestframework',
    #'debug_toolbar',
    'less',
    'ionyweb.administration',
    'ionyweb.authentication',
    'ionyweb.design',
    'ionyweb.file_manager',
    'ionyweb.website',
    'ionyweb.page',
    'ionyweb.plugin',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#---------------
# CONFIG TinyMCE
#---------------
TINYMCE_JS_URL = os.path.join(STATIC_URL, "tiny_mce/tiny_mce_src.js")
TINYMCE_JS_ROOT = os.path.join(get_ionyweb_path(), 'static', "tiny_mce")

TINYMCE_COMPRESSOR = True
TINYMCE_SPELLCHECKER = True
TINYMCE_FILEBROWSER = False
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,filemanager,paste,searchreplace,inlinepopups",
    'theme': "advanced",
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontsizeselect,|,forecolor,backcolor,|,bullist,numlist,|,outdent,indent,|,sub,sup,|,charmap,emotions,separator,forecolor,backcolor",
    'theme_advanced_buttons2' : "pastetext,pasteword,selectall,|,undo,redo,|,link,unlink,anchor,image,filemanager,code,|,tablecontrols,|,fullscreen",
    'theme_advanced_buttons3' : "",
    'relative_urls': False
}


#----------------------
# RENDERING PAGE ENGINE
#----------------------
RESTRICTED_THEMES = []

SLUG_PLACEHOLDER = 'placeholder'
SLUG_PLUGIN = 'plugin-relation'
SLUG_APP = 'app'
SLUG_CONTENT = 'content'
SLUG_DEFAULT = 'default'
SLUG_CLIPBOARD = 'clipboard'
SLUG_LAYOUT = 'layout'
SLUG_SEP = '-'

HTML_ID_PLACEHOLDER = '%s%s%s' % (SLUG_SEP, SLUG_PLACEHOLDER, SLUG_SEP)
HTML_ID_PLACEHOLDER_CONTENT = '%s%s' % (SLUG_CONTENT, HTML_ID_PLACEHOLDER)
HTML_ID_PLACEHOLDER_DEFAULT = '%s%s%s' % (SLUG_DEFAULT, SLUG_SEP, SLUG_PLACEHOLDER)
HTML_ID_PLACEHOLDER_CLIPBOARD = '%s%s%s' % (SLUG_CLIPBOARD, SLUG_SEP, SLUG_PLACEHOLDER)
HTML_ID_APP = '%s%s' % (SLUG_APP, SLUG_SEP)
HTML_ID_PLUGIN = '%s%s' % (SLUG_PLUGIN, SLUG_SEP)
HTML_ID_LAYOUT = '%s%s' % (SLUG_LAYOUT, SLUG_SEP)
HTML_ID_NAV = 'nav'

TEMPLATE_PLACEHOLDER_DEFAULT = 'layout/placeholder-default.html'
TEMPLATE_PLACEHOLDER_CLIPBOARD = 'layout/clipboard.html'
TEMPLATE_PLACEHOLDER = 'layout/placeholder.html'
TEMPLATE_APP = 'layout/placeholder-app.html'
TEMPLATE_PLUGIN = 'layout/plugin.html'
TEMPLATE_NAV_DEFAULT = 'navigation.html'
TEMPLATE_MAINTENANCE_DEFAULT = 'maintenance.html'
TEMPLATE_THEME_FILE_DEFAULT = 'index.html'
LAYOUT_DEFAULT = '100'

#------------------
# PAGE APP URL CONF
#------------------
SLUG_MIN_SIZE = 4
URL_PAGE_APP_SEP = u'p'
URL_ADMIN_SEP = u'wa'

ACTION_ADMIN_LIST_SUFFIX = '_list'
ACTION_ADMIN_ORDER_SLUG = '_order'
ADMIN_THEME = 'snow' # 'snow' || 'dark' || ... Will import ionyweb_admin_***.less

SITEMAP_INDEX = False

# ----------------
# PLUGINS SETTINGS
# ----------------
BREADCRUMB_PLUGIN = 'ionyweb.plugin_app.plugin_breadcrumb'
BREADCRUMB_OBJECT_TITLE = 'breadcrumb_object_title'

INPUT_FORMATS = ['%d/%m/%Y %H:%M', '%d-%m-%Y %H:%M']

# ---------------
# WEBSITE DOMAINS
# ---------------
RESTRICTED_DOMAINS = []

# ------------
# FILE MANAGER
# ------------
EXTENSIONS = {
    'Folder': [''],
    'Image': ['jpg','jpeg','gif','png'],
    'Audio': ['mpeg'],
    'Document': ['pdf','doc','xls','odt', 'ods', 'rtf','txt','csv'],
    'Archive': ['zip', 'rar', 'tar', 'tar.gz', '7z'],
    'Others': [],
    #'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
    #'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p']
}
DISPLAY_MODE = (
    (u"I", u"Icons"),
    (u"D", u"Details"),
    (u"L", u"Lists"),
)

VERSIONS = {
    'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop'},
    'thumbnail': {'verbose_name': 'Thumbnail (1 col)', 'width': 60, 'height': 60, 'opts': 'crop'},
    'small': {'verbose_name': 'Small (2 col)', 'width': 140, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (4col )', 'width': 300, 'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (6 col)', 'width': 460, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large (8 col)', 'width': 680, 'height': '', 'opts': ''},
    'croppedthumbnail': {'verbose_name': 'Cropped Thumbnail (300x200px)', 'width': 300, 'height': 200, 'opts': 'crop upscale'},
    'croppedthumb': {'verbose_name': 'Cropped Thumbnail (140x100px)', 'width': 140, 'height': 100, 'opts': 'crop upscale'},
    'croppedbig': {'verbose_name': 'Cropped big (450x323)', 'width': '', 'height': 323, 'opts': 'crop upscale'},
}

ADMIN_THUMBNAIL = 'admin_thumbnail'
VERSION_QUALITY = 90
IMAGE_MAXBLOCK = 1024*1024
FILE_MANAGER_QUOTA = "1073741824" #1024^3b = 1Gb












