# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from ionyweb.plugin_app.plugin_video.viewers.base import BaseViewer
import re

class YoutubeViewer(BaseViewer):

    @staticmethod
    def is_competent_for_url(url):
        """
        Return true for :
         - http://www.youtube.com/watch?v=S2VLEGtRuz4
         - http://www.youtube.com/watch?v=S2VLEGtRuz4&hd=1
         - http://www.youtube.com/watch?feature=player_embedded&v=-oGM6FBYLgM
         - http://www.youtube.com/watch?v=pb3WQ_b3Wqs
        """
        match = re.match('^(http://)?(www\.)?(youtube\.com/watch(.*)v=)(?P<id_video>[a-zA-Z0-9_-]+).*$', url)

        if match is not None:
            return True, match.group('id_video')
        return False, None

    @staticmethod
    def get_video_viewer(video_id):
        return mark_safe("""
            <iframe style="width:100%%; height: 100%%;"
            	src="http://www.youtube.com/embed/%s?wmode=transparent"
            	frameborder="0" wmode="Opaque" webkitAllowFullScreen allowfullscreen></iframe>""" % video_id)
