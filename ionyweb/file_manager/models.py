# -*- coding: utf-8 -*-
" File manager models"

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from django.conf import settings

from mptt.models import MPTTModel

import os
import shutil

# A directory is a node of our LIbrary File Tree.
# Can containt other Directory and file
class Directory(MPTTModel):
    
    parent = models.ForeignKey('self',
                               related_name='children',
                               db_index=True,
                               null=True,
                               blank=True,
                               help_text=_(u"Select the parent directory for this directory."))
    
    
    name = models.CharField(_(u"Folder Name"),
                            max_length=100,
                            help_text=_(u"Name of the folder"))
    
    def add_directory(self, name):
        new_dir = Directory.objects.create(name=name)
        new_dir.parent = self
        new_dir.save()
        
    def get_absolute_path(self):
        if self.parent:
            return self.parent.get_absolute_path() + "/" + self.name
        else:
            return self.filemanager.get().get_absolute_path()
        
    def size(self):
        calculated_size = 0
        for folder in self.children.all():
            calculated_size += folder.size()
        for file in self.files.all():
            if file and file.file():
                try:
                    calculated_size += file.file().file.size
                except IOError:
                    pass
            
        return calculated_size 
    
    def rename(self, new_name):
        self.name = new_name
        self.save()
    
    class Meta:
        verbose_name = _(u"Directory")
        verbose_name_plural = _(u'Directories')
        
    def __unicode__(self):
        return u'Directory'
    
    def delete(self, *args, **kwargs):
        if self.parent:
            for dir_child in self.children.all():
                dir_child.delete()
            for file_inside in self.files.all():
                file_inside.delete()
            super(Directory, self).delete(*args, **kwargs)

    
# FileManage have some method to manipulate data at a high level.
class FileManager(models.Model):
    
    root = models.ForeignKey(Directory,
                                  related_name="filemanager",
                                  default=None,
                                  blank=True,
                                  null=True)
    
    def delete(self, *args, **kwargs):
        shutil.rmtree(self.website.get().media_root())
        super(FileManager, self).delete(*args, **kwargs)
    
    def get_absolute_path(self):
        return self.website.get().media_root()
    
    def size(self):
        return self.root.size()
    
    class Meta:
        verbose_name = _(u"Files Library")
        verbose_name_plural = _(u'Files Libraries')

          
class File(models.Model):
    
    dir = models.ForeignKey(Directory,
                              related_name="files",
                              blank=False,
                              null=False)
    
    name = models.CharField(_(u'File name'), max_length=256, editable=False)  
    type = models.CharField(_(u'Type'), max_length=50, editable=False)
    
    date_creation = models.DateField(_(u'Creation date'), auto_now_add=True, editable=False)
    date_modification = models.DateField(_(u'Modification date'), auto_now=True, editable=False)

    file_type = models.ForeignKey(ContentType,
                                      related_name="file_file",
                                      limit_choices_to = {'model__startswith': 'file_manager_'},
                                      verbose_name=_("file_type"))
    file_id = models.PositiveIntegerField(editable=False)
    
    file_object = generic.GenericForeignKey('file_type', 'file_id')
 
    def file(self):
        try:
            tmp_fs_file_object = self.file_object.file.file

            return self.file_object.file
        except IOError:
            return None
    
    def get_icon(self):
        return self.file_object.get_icon()
         
    def get_thumbnail(self):
        website = self.dir.get_root().filemanager.get().website.get()
        return self.file_object.get_thumbnail(website)
    
    def get_thumbnail_icon(self):
        website = self.dir.get_root().filemanager.get().website.get()
        return self.file_object.get_thumbnail_icon(website)
       
    def get_absolute_url(self):
        return self.file_object.get_absolute_url()
    
    def get_selector_button(self):
        return self.file_object.get_selector_button()

    def rename(self, new_name):
        file_field_object = self.file()

        if not file_field_object:
            return None

        root, ext = os.path.splitext(new_name)
        new_filename = "%s_%d%s" % (slugify(root), self.id, ext)
        
        old_path = file_field_object.path
        new_path = "%s%s" % (os.path.join(file_field_object.path.strip(file_field_object.path.split("/")[-1])), new_filename)
        
        media_root = self.dir.get_root().filemanager.get().website.get().media_root()
        
        shutil.move(old_path, new_path)
        
        self.name = "%s%s" % (slugify(root), ext)
        file_field_object.name = os.path.join(media_root, new_filename)
        self.file_object.save()
        self.save()
        self.file_object.rename(old_path)
        # Rename all thumbnail
        
    
    def delete(self, *args, **kwargs):
        """
            Delete a file and all thumbnail associated
        """
        
        # Delete file
        self.file_object.delete()
        
        super(File, self).delete(*args, **kwargs)

    
class AbstractFile(models.Model):
    
    file = models.FileField(upload_to="file_manager/")
    
    def get_icon(self):
        return '<i class="icon-file icon-white"></i>'
    
    def get_thumbnail(self, website):
        return "<p>Aucun apercu disponible</p>"
    
    def get_thumbnail_icon(self, website):
        return '<img src="%sadmin/images/glyphicons/313_white.png" alt="%s" />' % (settings.STATIC_URL, self.file.name)
       
    
    def get_absolute_url(self):
        return os.path.join(settings.MEDIA_URL, self.file.name)
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super(AbstractFile, self).delete(*args, **kwargs)
    
    def get_selector_button(self):
        """
            Return selector button with multiple action in some case
        """
        html = render_to_string('administration/file_manager/selector/selector_button.html',
                                {'absolute_url': self.get_absolute_url(),})
        return html
    
    def rename(self, old_path):
        """
            No need to do any rename in a classic file type.
        """
        pass
    
    class Meta:
        abstract = True    

class Image(AbstractFile):
    #
    def get_icon(self):
        return '<i class="icon-picture icon-white"></i>'
    #

    def get_thumbnail(self, website):
        
        html = render_to_string('administration/file_manager/thumbnail/image.html',
                                {'file': self.file,
                                 'website': website})
        return html
   
    def get_thumbnail_icon(self, website):
        
        html = render_to_string('administration/file_manager/thumbnail/image_icon.html',
                                {'file': self.file,
                                 'website': website})
        return html
       
    def delete(self, *args, **kwargs):
        # Delete Thumbnail
        root, ext = os.path.splitext(self.file.path)
        image_list = []
        for label in settings.VERSIONS:
            image_list.append("%s_%s%s" % (root, label, ext))
        
        for file in image_list:
            try:
                os.remove(file)
            except:
                pass
              
        self.file.delete()
        super(AbstractFile, self).delete(*args, **kwargs)  
       
    def rename(self, old_path):
        """
            Rename all thumbnail linked to this image
        """
        old_root, old_ext = os.path.splitext(old_path)
        new_root, new_ext = os.path.splitext(self.file.path)

        for label in settings.VERSIONS:
            try:
                shutil.move("%s_%s%s" % (old_root, label, old_ext), "%s_%s%s" % (new_root, label, new_ext))
            except Exception,e:
                pass 
            
    def get_selector_button(self):
        """
            Return selector button with multiple action in some case
        """
        image_list = []
        for version in settings.VERSIONS:
            image_list.append([version, settings.VERSIONS[version]['verbose_name']])
        html = render_to_string('administration/file_manager/selector/selector_button_images.html',
                                {'absolute_url': self.get_absolute_url(),
                                 'versions': image_list,})
        return html
    
    class Meta:
        verbose_name = _(u"Image")
        verbose_name_plural = _(u'Images')
  

class Document(AbstractFile):
   
    #
    class Meta:
        verbose_name = _(u"Document")
        verbose_name_plural = _(u'Documents')
        
class Audio(AbstractFile):
    
    #
    def get_icon(self):
        return '<i class="icon-music icon-white"></i>'
    
    class Meta:
        verbose_name = _(u"Audio")
        verbose_name_plural = _(u'Audios')
        
#
class Archive(AbstractFile):
    
    #
    class Meta:
        verbose_name = _(u"Archive")
        verbose_name_plural = _(u'Archives')
        
#
class Other(AbstractFile):
    
    #
    class Meta:
        verbose_name = _(u"Other")
        verbose_name_plural = _(u'Others')
