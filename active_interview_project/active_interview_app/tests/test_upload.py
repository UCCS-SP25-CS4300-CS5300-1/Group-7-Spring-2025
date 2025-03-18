from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from active_interview_app.models import UploadedFile

#Run using python manage.py test active_interview_app.tests.test_upload

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