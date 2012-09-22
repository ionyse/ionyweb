"""
Authentication
"""

from django.test import TestCase
from django.test import Client

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class AuthenticationFormTest(TestCase):
    # def test_login_form(self):
    #     '''Test the login form'''
    #     response = self.client.get(reverse('auth_login'))
    #     self.assertEqual(response.status_code, 200)
    
    # def test_signup_form(self):
    #     '''Test the signup form'''
    #     response = self.client.get(reverse('auth_signup'))
    #     self.assertEqual(response.status_code, 200)

    # def test_account_activation(self):
    #     '''Test the user activation'''
    #     u = User.objects.create_user('username', 'username@user.com', 'password')
    #     response = self.client.get(reverse('auth_activation', 
    #                                        args=['1', '43d34ec8dd7b79871b663fb415496c1871ed2d05']))
    #     self.assertEqual(response.status_code, 200)
    pass
