from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from active_interview_app.models import UploadedFile, PastedText
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
import os
import unittest

#Run using python3 manage.py test active_interview_app.tests.test_upload

class FileUploadTestCase(TestCase):
    def test_file_upload(self):

        #This creates a text file to test for the upload functionality.
        test_file = SimpleUploadedFile("testfile.txt", b"This is the content of the file.", content_type="text/plain")
        #This sends the POST request to the upload endpoint.
        response = self.client.post(reverse('upload_file'), {'file': test_file}, format='multipart')

        #This checks for a successful redirect, which indicates that the POST was successful.
        self.assertEqual(response.status_code, 302)
        #This verifies that the file was properly saved.
        self.assertEqual(UploadedFile.objects.count(), 1)
        #This ensures the name of the uploaded file matches.
        uploaded_file = UploadedFile.objects.first()
        self.assertEqual(uploaded_file.file.name, "uploads/testfile.txt")




class PastedTextUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    def test_pasted_text_upload(self):
        # Simulate POST request to paste-text API endpoint
        response = self.client.post(reverse('save_pasted_text'), {
            'text': 'This is a test paste.'
        })

        # Redirect expected after success (302 to previous page)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PastedText.objects.count(), 1)

        # Check the created object
        pasted = PastedText.objects.first()
        self.assertEqual(pasted.content, 'This is a test paste.')
        self.assertEqual(pasted.user, self.user)

    def test_pasted_text_upload_blank(self):
        response = self.client.post(reverse('save_pasted_text'), {
            'text': ''
        })

        # Should redirect with error, but not save
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PastedText.objects.count(), 0)



class FileUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_upload_valid_pdf(self):
        self.client.login(username='testuser', password='testpass')
        pdf_file = SimpleUploadedFile("test.pdf", b"%PDF-1.4 test content", content_type="application/pdf")
        response = self.client.post(reverse('upload_file'), {'file': pdf_file}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "File uploaded successfully!")

    def test_upload_invalid_filetype(self):
        self.client.login(username='testuser', password='testpass')
        txt_file = SimpleUploadedFile("test.txt", b"Just some text", content_type="text/plain")
        response = self.client.post(reverse('upload_file'), {'file': txt_file}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid filetype")

class PastedTextViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_post_valid_text(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('pasted_text'), {'text': 'This is a pasted test.'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Text uploaded successfully!")

    def test_post_empty_text(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('pasted_text'), {'text': ''}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Text field cannot be empty")

class UploadedFileListTests(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        
    def test_get_uploaded_file_list(self):
        # Create an uploaded file for the user
        UploadedFile.objects.create(user=self.user, file="testfile.txt")
        
        # Send GET request to list uploaded files
        response = self.client.get(reverse('uploaded_file_list'))
        
        # Ensure status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure the file is in the response data
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['file'], 'testfile.txt')

class UploadedFileDetailTests(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.uploaded_file = UploadedFile.objects.create(user=self.user, file="testfile.txt")
        
    def test_get_uploaded_file(self):
        response = self.client.get(reverse('uploaded_file_detail', kwargs={'pk': self.uploaded_file.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file'], 'testfile.txt')

class PastedTextListTests(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        
    def test_get_pasted_text_list(self):
        # Create a pasted text entry
        PastedText.objects.create(user=self.user, content="Test paste")
        
        # Send GET request to list pasted texts
        response = self.client.get(reverse('pasted_text_list'))
        
        # Ensure status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure the pasted text is in the response data
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Test paste')

class PastedTextDetailTests(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.pasted_text = PastedText.objects.create(user=self.user, content="Test paste")
        
    def test_get_pasted_text(self):
        response = self.client.get(reverse('pasted_text_detail', kwargs={'pk': self.pasted_text.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test paste')

class UploadedFileListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_uploaded_file_list(self):
        # Create a file entry for the user
        uploaded_file = UploadedFile.objects.create(user=self.user, file='testfile.pdf')
        
        response = self.client.get(reverse('uploaded_file_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, uploaded_file.file.name)

    def test_post_uploaded_file(self):
        with open('testfile.pdf', 'wb') as f:
            f.write(b"PDF content")
        with open('testfile.pdf', 'rb') as f:
            response = self.client.post(reverse('uploaded_file_list'), {'file': f}, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UploadedFile.objects.count(), 1)
        uploaded_file = UploadedFile.objects.first()
        self.assertEqual(uploaded_file.file.name, 'testfile.pdf')

class UploadedFileDetailTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.uploaded_file = UploadedFile.objects.create(user=self.user, file='testfile.pdf')

    def test_get_uploaded_file_detail(self):
        response = self.client.get(reverse('uploaded_file_detail', kwargs={'pk': self.uploaded_file.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.uploaded_file.file.name)

    def test_put_uploaded_file(self):
        response = self.client.put(reverse('uploaded_file_detail', kwargs={'pk': self.uploaded_file.pk}),
                                   {'file': 'newfile.pdf'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.uploaded_file.refresh_from_db()
        self.assertEqual(self.uploaded_file.file.name, 'newfile.pdf')

    def test_delete_uploaded_file(self):
        response = self.client.delete(reverse('uploaded_file_detail', kwargs={'pk': self.uploaded_file.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(UploadedFile.objects.count(), 0)


class PastedTextListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_pasted_text_list(self):
        pasted_text = PastedText.objects.create(user=self.user, content='Test paste')
        
        response = self.client.get(reverse('pasted_text_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, pasted_text.content)

    def test_post_pasted_text(self):
        response = self.client.post(reverse('pasted_text_list'), {'content': 'Another test paste'}, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PastedText.objects.count(), 1)
        pasted_text = PastedText.objects.first()
        self.assertEqual(pasted_text.content, 'Another test paste')


class PastedTextDetailTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.pasted_text = PastedText.objects.create(user=self.user, content='Test paste')

    def test_get_pasted_text_detail(self):
        response = self.client.get(reverse('pasted_text_detail', kwargs={'pk': self.pasted_text.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pasted_text.content)

    def test_put_pasted_text(self):
        response = self.client.put(reverse('pasted_text_detail', kwargs={'pk': self.pasted_text.pk}),
                                   {'content': 'Updated paste'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.pasted_text.refresh_from_db()
        self.assertEqual(self.pasted_text.content, 'Updated paste')

    def test_delete_pasted_text(self):
        response = self.client.delete(reverse('pasted_text_detail', kwargs={'pk': self.pasted_text.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(PastedText.objects.count(), 0)


class IndexViewTest(TestCase):
    def test_index_view(self):
        # Send GET request to the 'index' view
        response = self.client.get(reverse('index'))
        
        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'index.html')

class FileUploadTestCase(TestCase):
    def test_file_upload_form_instantiation(self):
        # Simulate a GET request, where the form should be instantiated
        response = self.client.get(reverse('upload_file'))  # Adjust this to your actual URL name
        
        # Ensure the response status is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check if the form is in the context, indicating that it was instantiated
        self.assertIn('form', response.context)

