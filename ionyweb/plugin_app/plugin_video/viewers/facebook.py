# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from ionyweb.plugin_app.plugin_video.viewers.base import BaseViewer
import re

class FacebookViewer(BaseViewer):

    @staticmethod
    def is_competent_for_url(url):
        """
        Return true for :
            - https://www.facebook.com/video/video.php?v=1498994573921
        """
        match = re.match('^(http(s?)://)?(www\.)?(facebook\.com/(.*)\?v=)(?P<id_video>\d+).*$', url)

        if match is not None:
            return True, match.group('id_video')
        return False, None

    @staticmethod
    def get_video_viewer(video_id):
        return mark_safe("""
           <iframe src="http://www.facebook.com/v/%s"
           	style="width: 100%%; height: 100%%;" frameborder="0"
           	webkitAllowFullScreen allowFullScreen></iframe>""" % video_id)
