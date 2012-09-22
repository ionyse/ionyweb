# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from ionyweb.administration.tests import test_reverse, AdministrationTests

class LoginViewTests(AdministrationTests):

    def test_login_view(self):
        """Ensure the robots view exists"""
        url = test_reverse('wa-login')

        # Bad login
        response = self.client.post(url, {'email': 'badlogin', 'password': 'admin'})
        self.assertContains(response, 'msg', status_code=400)

        # Bad password
        response = self.client.post(url, {'email': 'contact@ionyse.com', 'password': 'badpassword'})
        self.assertContains(response, 'msg', status_code=400)

        # Inactive account
        user = User.objects.create_user(username='login', email='foo@bar.com', password='foobar')
        user.is_active = False
        user.save()
        response = self.client.post(url, {'email': 'foo@bar.com', 'password': 'foobar'})
        self.assertContains(response, 'msg', status_code=400)

        # Connection OK
        response = self.client.post(url, {'email': 'contact@ionyse.com', 'password': 'admin'})
        self.assertContains(response, 'msg')
