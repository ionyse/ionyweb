# -*- coding: utf-8 -*-

class BaseViewer(object):

    @staticmethod
    def is_competent_for_url(url):
        raise NotImplementedError('Please extends the is_competent_for_url method')

    @staticmethod
    def get_video_viewer(video_id):
        raise NotImplementedError('Please extends the get_video_viewer method')
        
