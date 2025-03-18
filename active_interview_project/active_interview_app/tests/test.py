from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginTest(TestCase):
    def testlogin(self):
        self.user = User.objects.create_user(username='craig', password='1')
        login = self.client.login(username='craig', password='1')
        self.assertTrue(login)
       
    def testlogout(self):
        logout = self.client.logout()
        self.assertTrue(logout == None)
        

    