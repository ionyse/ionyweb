# -*- coding: utf-8 -*-

from ionyweb.administration.views import IsSuperAdminView
from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status
from django.conf import settings

from django.template.loader import render_to_string
from django.template import RequestContext

from ionyweb.administration.utils import MESSAGES
from ionyweb.file_manager.models import File, Directory
from ionyweb.file_manager.views import (render_quota_html,
                                       render_directories_list_html,
                                       render_files_list_html)
from ionyweb.file_manager.functions import get_path_or_create

class FileManagerQuota(IsSuperAdminView):
    
    def get(self, request):
        # Render HTML        
        
        quota = render_quota_html(request)
        
        response = Response(status.HTTP_200_OK, {"quota": quota})
        return self.render(response)
    
    
class FileManagerPanel(IsSuperAdminView):
    
    def get(self, request):
        # Render HTML
        
        directory_list = render_directories_list_html(request)
        
        files_list = render_files_list_html(request)
        
        quota = render_quota_html(request)
        
        selector = False
        if 'selector' in request.GET:
            selector = True
        
        html = render_to_string('administration/file_manager/index.html',
                                {'files_list': files_list,
                                 'quota': quota,
                                 'directory_list': directory_list,
                                 'selector': selector},
                                context_instance = RequestContext(request))
        
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
    def post(self, request):
        """
            Use to move file or directory in filemanager tree
        """
        
        drop = request.POST.get('drop')
        inside = request.POST.get('in')
        current_dir = request.POST.get('current')
        
        dir_inside = Directory.objects.get(pk=inside.strip('dir-')) 
        
        if drop.startswith('dir-'):
            dir_drop = Directory.objects.get(pk=drop.strip('dir-'))
            dir_drop.parent = dir_inside
        else:
            dir_drop = File.objects.get(pk=drop)
            dir_drop.dir = dir_inside
        dir_drop.save()
                    
        directory_list = render_directories_list_html(request, current_dir)
                    
        response = Response(status.HTTP_200_OK, {"directory_list": directory_list})
        return self.render(response)

class FileManagerFile(IsSuperAdminView):
    
    def get(self, request, pk=None): 
        
        managed_file = File.objects.get(pk=pk)
         
        selector = None
        if 'selector' in request.GET and request.GET.get('selector') == 'true':
            selector = managed_file.get_selector_button()
        
        html = render_to_string('administration/file_manager/file_details.html',
                                {'file': managed_file,
                                 'selector': selector},
                                context_instance = RequestContext(request)) 
         
        response = Response(status.HTTP_200_OK, {"html": html})
        return self.render(response)
    
    def post(self, request, pk):
        
        managed_file = File.objects.get(pk=pk)
        
        managed_file.rename(request.POST.get('name'))
        
        response = Response(status.HTTP_200_OK, {"msg": "ok"})
        return self.render(response)
    
    def delete(self, request, pk):
        managed_file = File.objects.get(pk=pk)
        managed_file.delete()
        
        quota = render_quota_html(request)
        
        response = Response(status.HTTP_200_OK, {"quota": quota})
        return self.render(response)
        
  
class FileManagerDirectory(IsSuperAdminView):
    
    # Return all files in id directory
    def get(self, request, pk=None):
        # First, get the directory object and check if is owned by request.website
        if pk == "0":
            managed_dir = request.website.file_manager().root
        else:
            managed_dir = Directory.objects.get(pk=pk)
        if managed_dir.get_root().filemanager.get().website.get() != request.website:
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST,
                                {'msg': MESSAGES.get('default_error', "")})
        
        # Check User display mode for filemanager (NOt implemented yet)
        #
        # mode = request.user.profile.get().file_manager_display_mode
        
        # Generate templates
        files_list = render_files_list_html(request, managed_dir)
    
        # Return html code width status.HTTP_200_OK
        response = Response(status.HTTP_200_OK, {"html": files_list})
        return self.render(response)
    
    
    # Create a new directory with id as parent
    def put(self, request, pk=None):  
        
        if pk == "0":
            managed_dir = request.website.file_manager().root
        else:
            managed_dir = Directory.objects.get(pk=pk)
            
        new_dir = Directory()
        new_dir.name = ""
        new_dir.parent = managed_dir
        new_dir.save()
        
        files_list = render_files_list_html(request, managed_dir)
        directory_list = render_directories_list_html(request)
        # Return html code width status.HTTP_200_OK
        response = Response(status.HTTP_200_OK, {"files_list": files_list, "directory_list": directory_list, 'id': new_dir.id})
        return self.render(response)
    
    # Edit a directory. Can be renamed, moved, ...
    def post(self, request, pk=None):
        
        if pk == "0":
            managed_dir = request.website.file_manager().root
        else:
            managed_dir = Directory.objects.get(pk=pk)
        
        managed_dir.rename(request.POST.get('name'));
               
        
        files_list = render_files_list_html(request, managed_dir.parent)
        directory_list = render_directories_list_html(request)
        
        # Return html code width status.HTTP_200_OK
        response = Response(status.HTTP_200_OK, {"files_list": files_list, "directory_list": directory_list})
        
        return self.render(response)    
    # Delete a directory. Also delete all files inside
    def delete(self, request, pk):
        
        Directory.objects.get(pk=pk).delete()
        
        directory_list = render_directories_list_html(request)
        
        quota = render_quota_html(request)
        
        # Return html code width status.HTTP_200_OK
        response = Response(status.HTTP_200_OK, {"directory_list": directory_list, "quota": quota})
        return self.render(response)
 
    
class FileManagerThumbnailFile(IsSuperAdminView):
    
    def get(self, request):
        
        path = request.GET.get('path')
        size = request.GET.get('size')
        
        thumbnail = get_path_or_create(path.strip(settings.MEDIA_URL), size, path.strip(settings.MEDIA_URL)[:-len(path.split("/")[-1])])

        # Return html code width status.HTTP_200_OK
        response = Response(status.HTTP_200_OK, {"thumbnail": "%s%s" % (settings.MEDIA_URL, thumbnail)})
        return self.render(response)   


class FileManagerDisplayMode(IsSuperAdminView):
    
    
    def post(self, request):
        
        mode = request.POST.get('mode')
        
        list_mode = []
        for i in settings.DISPLAY_MODE:
            list_mode.append(i[0])
        
        if mode in list_mode:
            profile = request.user.profile.get()
            profile.file_manager_display_mode = mode
            profile.save()
            
            response = Response(status.HTTP_200_OK)
            return self.render(response) 
        
        else:
            response = Response(status.HTTP_404_NOT_FOUND)
            return self.render(response) 
