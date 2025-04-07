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


class RegisterViewTests(TestCase):
    def setUp(self):
        # Create the 'manager_role' group before testing
        self.group = Group.objects.create(name='manager_role')
        # URL for the registration view
        self.url = reverse('register')

    def test_register_valid_user(self):
        # Valid user data for registration
        data = {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        # Send POST request to register view
        response = self.client.post(self.url, data)

        # Check that the user was successfully created and redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Check that the user exists in the database
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)

        # Check that the user is added to the 'manager_role' group
        self.assertTrue(self.group in user.groups.all())

        # Check that a success message was added to the messages queue
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Account was created for newuser')

    def test_register_invalid_user(self):
        # Invalid user data for registration (passwords do not match)
        data = {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
        }

        # Send POST request to registration view
        response = self.client.post(self.url, data)

        # Check that the page is re-rendered with form errors (status 200)
        self.assertEqual(response.status_code, 200)

        # Check that the form has errors
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

        # Ensure no user is created in the database
        self.assertEqual(User.objects.count(), 0)

    def test_register_email_sent_on_success(self):
        # Valid user data for registration
        data = {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        # Send POST request to register view
        response = self.client.post(self.url, data)

        # Check that the user was created
        user = User.objects.get(username='newuser')

        # Check if an email was sent (Django sends a confirmation email after user creation)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Welcome', mail.outbox[0].subject)