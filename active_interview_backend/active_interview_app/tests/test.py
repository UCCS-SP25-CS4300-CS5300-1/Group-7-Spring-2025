from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from django.core import mail


class LoginTest(TestCase):
    def testregister(self):
        register = User.objects.create_user(username='craig', password='1')
        self.assertTrue(register != None)

    def testlogin(self):
        User.objects.create_user(username='craig', password='1')
        login = self.client.login(username='craig', password='1')
        
        self.assertTrue(login)

    def testlogout(self):
        User.objects.create_user(username='craig', password='1')
        self.client.login(username='craig', password='1')
        logout = self.client.logout()
        self.assertTrue(logout == None)
    
    def testfaillogin(self):
        User.objects.create_user(username='craig', password='1')
        login = self.client.login(username='craig', password='2')
        self.assertFalse(login)

        

    