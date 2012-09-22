# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_protect
from django.conf.urls import patterns, url
from ionyweb.administration.views.login import LoginView, LogoutView
from ionyweb.administration.views.page import PagesView, PageView, PageLayoutView
from ionyweb.administration.views.plugin import (PluginView, PluginsView, PluginsByCategoryView, PluginsDescription,
                                                PluginRelationView)
from ionyweb.administration.views.action import ActionView
from ionyweb.administration.views.apps import PageAppView
from ionyweb.administration.views.design import (DesignList,
                                                DesignStylesList)
from ionyweb.administration.views.manifest import (LayoutsListView, 
                                                  LayoutListView)
from ionyweb.administration.views.users import CurrentUser
from ionyweb.administration.views.test import TestView
from ionyweb.administration.views.file_manager import (FileManagerPanel,
                                                      FileManagerDirectory,
                                                      FileManagerFile,
                                                      FileManagerThumbnailFile,
                                                      FileManagerDisplayMode)
from ionyweb.administration.views.website import (Domains, Domain, Versions, 
                                                 Analytics, Referencement,
                                                 Maintenance)

urlpatterns = patterns(
    '',

    # Manifest Layout and Themes actions
    url(r'^layouts/$', csrf_protect(LayoutsListView.as_view()), name='wa-layouts'),
    url(r'^layout/$', csrf_protect(LayoutListView.as_view()), name='wa-layout'),
    #url(r'^themes/$', csrf_protect(ThemesListView.as_view()), name='wa-themes'),


    # --------------------
    # FIXUS :
    # Update and tests required for
    # the following items..
    # --------------------
    

    # Login actions
    url(r'^login/$', LoginView.as_view(), name='wa-login'),
    url(r'^logout/$', LogoutView.as_view(), name='wa-logout'),

    # Menu actions
    # url(r'^menu/$', 'menu'),
    # url(r'^menu/(?P<slug>[a-zA-Z_\-]*)/$', 'menu'),
    
    # Plugin actions
    url(r'plugin/$', PluginView.as_view(), name='wa-plugin'),
    url(r'plugin/(?P<relation_html_id>[a-zA-Z0-9_\-]*)/$', PluginView.as_view(), name='wa-plugin'),
    url(r'plugins/$', PluginsView.as_view(), name='wa-plugins'),
    url(r'plugins/category/(?P<slug>[a-zA-Z0-9_\-]*)/$', PluginsByCategoryView.as_view(), name='wa-plugins-category'),
    url(r'plugins/description/(?P<id>[a-zA-Z0-9_\-]*)/$', PluginsDescription.as_view(), name='wa-plugins-description'),
    url(r'plugin-page-relation/$', PluginRelationView.as_view(), name='wa-plugin-page-relation'),

    # Actions Admin
    url(r'action/(?P<html_id_object>[a-zA-Z0-9_\-]*)/(?P<url_action>.*)$',
        csrf_protect(ActionView.as_view()), name='wa-actions'),

    # Page App actions
    url(r'page_app/(?P<page_pk>\d+)/$', PageAppView.as_view(), name='wa-page-app'),
    url(r'page_app/$', PageAppView.as_view(), name='wa-page-app'),
    
    # Page actions
    url(r'pages/$', PagesView.as_view(), name='wa-pages'),
    
    url(r'page/$', csrf_protect(PageView.as_view()), name='wa-page'),
    url(r'page/(?P<pk>\d+)/$', csrf_protect(PageView.as_view()), name='wa-page'),
    #url(r'page/duplicate/(?P<pk>\d+)/$', PageDuplicateView.as_view(), name='wa-page-duplicate'),
    
    url(r'page/layout/$', PageLayoutView.as_view(), name='wa-page-layout'),

    url(r'website/domains/$', Domains.as_view(), name='wa-domains'),
    url(r'website/domain/$', Domain.as_view(), name='wa-domain'),
    url(r'website/domain/(?P<pk>\d+)/$', Domain.as_view(), name='wa-domain'),
    url(r'website/versions/$', Versions.as_view(), name='wa-versions'),
    url(r'website/analytics/$', Analytics.as_view(), name='wa-analytics'),
    url(r'website/referencement/$', Referencement.as_view(), name='wa-referencement'),
    url(r'website/maintenance/$', Maintenance.as_view(), name='wa-maintenance'),
    
    url(r'users/currentUser/$', CurrentUser.as_view(), name='wa-current-user'),

    # Design section
    url(r'designs/$', DesignList.as_view(), name='wa-design-list'),
    url(r'design/$', DesignStylesList.as_view(), name='wa-design-styles'),
    url(r'design/(?P<pk>[a-zA-Z0-9_\-]*)/$', DesignStylesList.as_view(), name='wa-design-styles'),
    url(r'design/(?P<pk>[a-zA-Z0-9_\-]*)/preview/$', DesignList.as_view(), name='wa-design-preview-styles'),
    url(r'design/(?P<pk>[a-zA-Z0-9_\-]*)/preview/(?P<styles_slug>\d+)/$', DesignList.as_view(), name='wa-design-preview-styles'),
    url(r'design/(?P<pk>[a-zA-Z0-9_\-]*)/save/$', DesignList.as_view(), name='wa-design-save-styles'),
    url(r'design/(?P<pk>[a-zA-Z0-9_\-]*)/save/(?P<styles_slug>\d+)/$', DesignList.as_view(), name='wa-design-save-styles'),
    
    # File Manager section
    url(r'file_manager/$', FileManagerPanel.as_view(), name='wa-file-manager-list'),
    url(r'file_manager/upload/$', 'ionyweb.file_manager.views.upload_file', name='wa-file-manager-add'),
    url(r'file_manager/upload/(?P<directory_id>\d+)/$', 'ionyweb.file_manager.views.upload_file', name='wa-file-manager-add'),
    url(r'file_manager/dir/(?P<pk>\d+)/$', FileManagerDirectory.as_view(), name='wa-file-manager-dir'),
    url(r'file_manager/file/(?P<pk>\d+)/$', FileManagerFile.as_view(), name='wa-file-manager-file'),
    url(r'file_manager/thumbnail/$', FileManagerThumbnailFile.as_view(), name='wa-file-manager-thumb'),
    url(r'file_manager/display/$', FileManagerDisplayMode.as_view(), name='wa-file-manager-display-mode'),


    url(r'^test/(?P<status_code>\d+)/$', TestView.as_view(), name='wa-tests'),
)
