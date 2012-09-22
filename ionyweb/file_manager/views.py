# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from ionyweb.file_manager.models import File, Directory, Document, Image, Audio, Archive, Other
from ionyweb.file_manager.functions import storage as default_storage
from ionyweb.administration.utils import MESSAGES
from django.conf import settings
from django.utils.translation import ugettext as _

import magic
import os.path
import os
import time
# JSON import
try:
    import json
except ImportError:
    from django.utils import simplejson as json

def render_quota_html(request):
    
    root = request.website.file_manager().root
        
    return render_to_string('administration/file_manager/quota.html',
                                {'root': root,
                                 'maxquota': settings.FILE_MANAGER_QUOTA},
                                context_instance = RequestContext(request))

def render_directories_list_html(request, current=None):
    
    root = request.website.file_manager().root
    if current and current != '0':
        current = Directory.objects.get(pk=current)
    else:
        current = root    
        
    return render_to_string('administration/file_manager/directory_list.html',
                                {'root': root,
                                 'directories': root.get_descendants(),
                                 'current': current},
                                context_instance = RequestContext(request))
    
def render_files_list_html(request, directory=False, selector=False):
    
    if directory is False:
        directory = request.website.file_manager().root
    
    if request.user.profile.get().file_manager_display_mode == "I":
        template = 'administration/file_manager/files_list_icons.html'
    else:
        template = 'administration/file_manager/files_list.html'
    
    return render_to_string(template,
                                {'directory': directory,
                                 'selector': selector,
                                 'folders': directory.children.all().order_by('name'),
                                 'files': directory.files.all().order_by('name')},
                                context_instance = RequestContext(request))

def upload_file(request, directory_id=0):
    """
    Upload file to the server.
    """
    if request.method == "POST":
        if request.is_ajax(): # Advanced (AJAX) submission
            filedata = ContentFile(request.body)
            try:
                filedata.name = request.GET['qqfile']
            except KeyError:
                return HttpResponseBadRequest('Invalid request! No filename given.')
        else: # Basic (iframe) submission
            # TODO: This needs some attention, do we use this at all?
            if len(request.FILES) == 1:
                filedata = request.FILES.values()[0]
            else:
                raise Http404('Invalid request! Multiple files included.')
            filedata.name = request.POST.get('file_name')

        filename = filedata.name
        root, ext = os.path.splitext(filename)
        ext = ext.lower()

        file_model = File()    
        if directory_id == 0:
            file_model.dir = request.website.file_manager().root
        else:
            file_model.dir = get_object_or_404(Directory, pk=directory_id)
            
        file_model.name = str(time.time()).replace(".","")    
        file_path = "%s/%s%s" % (request.website.file_manager().root.get_absolute_path(), 
                                 file_model.name, ext)
        new_file = default_storage.save(file_path, filedata)

        #file_model.name = "%s%s" % (slugify(root), ext)

        mime = magic.Magic(mime=True)
        content_type = mime.from_file(default_storage.path(new_file))
        file_model.type = content_type
        type, extension = content_type.split('/')

        if extension in settings.EXTENSIONS['Image']:
            file_type = Image()
        elif extension in settings.EXTENSIONS['Audio']:
            file_type = Audio()
        elif extension in settings.EXTENSIONS['Document']:
            file_type = Document()
        elif extension in settings.EXTENSIONS['Archive']:
            file_type = Archive()
        elif extension in settings.EXTENSIONS['Others']:
            file_type = Other()
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, new_file))
            #file_type = Other()
            # _('Today is %(month)s %(day)s.') % {'month': m, 'day': d}
            ret_json = {"error": _(u"This file is %(type)s/%(extension)s type and is not allow in file manager.")  % {'type': type, 'extension': extension}}
            return HttpResponse(json.dumps(ret_json))

        file_type.file = new_file
        file_type.save()

        file_model.file_type = ContentType.objects.get_for_model(file_type)
        file_model.file_id = file_type.id
        file_model.save()
        file_model.rename("%s%s"% (slugify(root), ext))
        #Save it
        quota = render_quota_html(request)

        # let Ajax Upload know whether we saved it or not
        ret_json = {"quota": quota, "success": True}
        return HttpResponse(json.dumps(ret_json))
    else:
        html = render_to_string('administration/file_manager/files_upload.html',
                                {},
                                context_instance = RequestContext(request))

        ret_json = {"html": html}
        return HttpResponse(json.dumps(ret_json), mimetype="application/json")
