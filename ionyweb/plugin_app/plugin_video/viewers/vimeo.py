# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from ionyweb.plugin_app.plugin_video.viewers.base import BaseViewer
import re

class VimeoViewer(BaseViewer):

    @staticmethod
    def is_competent_for_url(url):
        """
        Return true for :
            - http://vimeo.com/17065523
        """
        match = re.match('^(http://)?(www\.)?(vimeo\.com/)(?P<id_video>\d+).*$', url)

        if match is not None:
            return True, match.group('id_video')
        return False, None

    @staticmethod
    def get_video_viewer(video_id):
        return mark_safe("""
           <iframe src="http://player.vimeo.com/video/%s?title=0&amp;byline=0&amp;portrait=0"
           	style="width: 100%%; height: 100%%;" frameborder="0"
           	webkitAllowFullScreen allowFullScreen></iframe>""" % video_id)
