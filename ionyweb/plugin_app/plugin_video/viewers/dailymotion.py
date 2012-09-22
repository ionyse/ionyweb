# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from ionyweb.plugin_app.plugin_video.viewers.base import BaseViewer
import re

class DailymotionViewer(BaseViewer):

    @staticmethod
    def is_competent_for_url(url):
        """
        Return true for :
            - http://www.dailymotion.com/video/xfoi91
            - http://www.dailymotion.com/video/xfoi91_zapping-du-18-novembre-2010_news#hp-v-v1
        """
        match = re.match('^(http://)?(www\.)?(dailymotion\.com/video/)(?P<id_video>[a-zA-Z0-9]+).*$', url)

        if match is not None:
            return True, match.group('id_video')
        return False, None

    @staticmethod
    def get_video_viewer(video_id):
        return mark_safe("""
            <iframe style="width: 100%%; height: 100%%"
        	    frameborder="0" webkitAllowFullScreen allowFullScreen
        	    src="http://www.dailymotion.com/embed/video/%s"></iframe>""" % video_id)
