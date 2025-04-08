from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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


class TestFeaturesPage(TestCase):
    def testGETFeaturesPage(self):
        # Call the view with a response
        response = self.client.get(reverse('features'))

        # Validate that the view is valid
        self.assertEqual(response.status_code, 200)

        # Validate that the index template was used
        self.assertTemplateUsed(response,'base.html')
        

    