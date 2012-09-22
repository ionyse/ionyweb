# -*- coding: utf-8 -*-

import floppyforms as forms
from ionyweb.forms import ModuloModelForm
from django.utils.translation import ugettext_lazy as _
from ionyweb.plugin_app.plugin_video.models import (Plugin_Video, 
                                                   VIDEO_TYPE_CHOICES, 
                                                   VIDEO_VIEWERS)

import requests


class Plugin_VideoForm(ModuloModelForm):
    
    def save(self, *args, **kwargs):

        video = super(Plugin_VideoForm, self).save(*args, commit=False, **kwargs)
        video.id_video = self.cleaned_data['id_video']
        video.video_type = self.cleaned_data['video_type']
        if kwargs.get('commit', True):
            video.save()

        return video


    def clean(self):
        
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url", u"")

        # Try if the url was shortened
        request = requests.get(url)
        redirected_url = request.url

        video_viewer_found = False

        for video_type, viewer_class in VIDEO_VIEWERS.items():
            is_driver, video_id = viewer_class.is_competent_for_url(url)
            if is_driver:
                cleaned_data['video_type'] = video_type
                cleaned_data['id_video'] = video_id
                video_viewer_found = True
                break
            
            is_driver, video_id = viewer_class.is_competent_for_url(redirected_url)
            if is_driver:
                cleaned_data['video_type'] = video_type
                cleaned_data['id_video'] = video_id
                cleaned_data['url'] = redirected_url
                video_viewer_found = True
                break
            

        if not video_viewer_found:
            self._errors['url'] = self.error_class([
                    _(u"The video URL could not be recognised. "
                      u"Make sure it is a %(video_types)s valid URL." % {
                            'video_types': ', '.join([v[1] for v in VIDEO_TYPE_CHOICES])})])

        return cleaned_data


    def clean_width_video(self):
        data = self.cleaned_data['width_video']
        if data > Plugin_Video.MAX_WIDTH_VIDEO:
            raise forms.ValidationError(_(u"Max width : %s pixels." % Plugin_Video.MAX_WIDTH_VIDEO))
        return data


    def clean_height_video(self):
        data = self.cleaned_data['height_video']
        if data > Plugin_Video.MAX_HEIGHT_VIDEO:
            raise forms.ValidationError(_(u"Max height : %s pixels." % Plugin_Video.MAX_HEIGHT_VIDEO))
        return data
        

    class Meta:
        model = Plugin_Video
        exclude = ('video_type', 'id_video')

