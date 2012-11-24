"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TransactionTestCase

from ionyweb.website.models import WebSite
from django.contrib.sites.models import Site
from ionyweb.file_manager.models import FileManager, Directory
from django.contrib.auth.models import User

import os

class SimpleTest(TransactionTestCase):
    
    def setUp(self):
        # Flush databases
        
        # Create website with a IonywebSubscription home page
        # Create the domain name
        site = Site.objects.get_or_create(pk=1)[0]
        site.domain = "testserver"
        site.name = "Notmyidea"
        site.save()
    
        # Create the website
        self.website = WebSite.objects.create(
            title="Notmyidea", theme="notmyidea",
            default_layout="100", slug="notmyidea", 
            domain=site)
        self.website.ndds.add(site)
    
    def test_file_manager_getter_with_creation(self):
        # Test if accessible an empty file library automaticaly create one
        self.assertEqual(self.website.files_library, None)
        self.website.file_manager()
        self.assertNotEqual(self.website.files_library, None)
        
    def test_file_manager_creation_media_root(self):
        # Create fileManager to create media_root file
        self.website.file_manager()
        # TEst if mediaroot file exist and is a folder
        self.assertEqual(os.path.isdir(self.website.media_root()), True)

    def test_file_manager_get_list_folder(self):
        # Test liste of directory from root media directory
        self.assertEqual(self.website.file_manager().root.children.count(), 0)

    def test_file_manager_display_mode(self):
        # Test if user has by default List mode for File Manager Display Mode
        user = User.objects.create(username='login', email='foo@bar.com', password='foobar', is_active=False)
        self.assertEqual(user.profile.get().file_manager_display_mode, "L")
        
    def test_file_manager_create_directory(self):
        # Create a sub-directory to an existing one
        self.website.file_manager().root.add_directory('folder1')
        self.assertEqual(self.website.file_manager().root.children.count(), 1)
        self.assertEqual(self.website.file_manager().root.children.get().name, 'folder1')

    def test_do_upload(self):
        # ## Attemp an upload using AJAX SUBMISSION
        # f = open(os.path.join(os.dirname(__file__), 'img/testimage.jpg'), "rb")
        # file_size = os.path.getsize(f.name)
        # url = reverse('wa-upload', 'ionyweb.administration.urls')
        # url = '?'.join([url, urlencode({'qqfile': 'testimage.jpg'})])
        # response = test.c.post(url, data=f.read(), content_type='application/octet-stream', HTTP_X_REQUESTED_WITH='XMLHttpRequest', X_File_Name='testimage.jpg')
        # f.close()
    
        # # Check we get OK response
        # test.assertTrue(response.status_code == 200)
    
        # # Check the file now exists
        # path = os.path.join(test.tmpdir.path, 'testimage.jpg')
        # test.testfile = FileObject(path, site=test.site)
        # test.assertTrue(test.site.storage.exists(path))
    
        # # Check the file has the correct size
        # test.assertTrue(file_size == test.site.storage.size(path))
        pass
