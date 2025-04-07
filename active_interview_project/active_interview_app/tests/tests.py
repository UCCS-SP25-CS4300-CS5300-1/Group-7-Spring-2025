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

class UploadedFileListAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Authenticate the client with the test user
        self.client.force_authenticate(user=self.user)
        # Define the URL for the 'UploadedFileList' view
        self.url = reverse('upload_file_list')  # Make sure 'upload_file_list' matches the name in your URL config

    def test_post_upload_file(self):
        # Prepare a sample file for upload
        test_file = SimpleUploadedFile("testfile.txt", b"This is the content of the file.", content_type="text/plain")
        
        # Send POST request to upload the file
        response = self.client.post(self.url, {'file': test_file}, format='multipart')

        # Ensure the file was uploaded successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that the file is saved in the database
        uploaded_file = UploadedFile.objects.first()
        self.assertEqual(uploaded_file.file.name, "uploads/testfile.txt")
        self.assertEqual(uploaded_file.user, self.user)  # Ensure the file is associated with the correct user

    def test_post_invalid_file_upload(self):
        # Send POST request with invalid file type (e.g., text file instead of PDF)
        test_file = SimpleUploadedFile("test.txt", b"Just some text", content_type="text/plain")
        
        response = self.client.post(self.url, {'file': test_file}, format='multipart')
        
        # Check that the file upload was rejected due to invalid file type (assuming validation in the view)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)