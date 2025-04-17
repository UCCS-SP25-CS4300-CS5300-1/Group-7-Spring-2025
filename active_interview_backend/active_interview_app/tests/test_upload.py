from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from active_interview_app.models import UploadedJobListing, UploadedResume
from django.test import TestCase, Client
from django.contrib.messages import get_messages
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
import os
import unittest
import shutil


#Run using python3 manage.py test active_interview_app.tests.test_upload

class ResumeUploadTestCase(TestCase):
    def test_file_upload(self):
        test_file = SimpleUploadedFile("testfile.txt", b"This is the content of the file.", content_type="text/plain")
        response = self.client.post(reverse('upload_file'), {'file': test_file}, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UploadedResume.objects.count(), 1)
        uploaded_file = UploadedResume.objects.first()
        self.assertEqual(uploaded_file.file.name, "uploads/testfile.txt")


class UploadedJobListingUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

def test_pasted_text_upload(self):
    response = self.client.post(reverse('save_pasted_text'), {
        'paste-text': 'This is a test paste.',
        'title': 'Sample Title'
    }, follow=True)

    self.assertEqual(response.status_code, 200)

    messages_list = list(messages.get_messages(response.wsgi_request))
    self.assertTrue(any("Text uploaded successfully!" in str(m) for m in messages_list))
    pasted = UploadedJobListing.objects.first()
    self.assertEqual(pasted.content, 'This is a test paste.')
    self.assertEqual(pasted.user, self.user)

    def test_pasted_text_upload_blank(self):
        response = self.client.post(reverse('save_pasted_text'), {
            'paste-text': ''
        })

        # Should redirect with error, but not save
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UploadedJobListing.objects.count(), 0)


class ResumeUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_upload_valid_pdf(self):
        print(f"Current working directory: {os.getcwd()}")
        pdf_path = os.path.join(os.getcwd(), 'active_interview_app', 'tests', 'test.pdf')

        self.assertTrue(os.path.exists(pdf_path), f"Test PDF file not found at {pdf_path}")

        with open(pdf_path, 'rb') as pdf_file:
            uploaded_pdf = SimpleUploadedFile('test.pdf', pdf_file.read(), content_type='application/pdf')

        self.client.login(username='testuser', password='testpass')

        response = self.client.post(
            reverse('upload_file'),
            {
                'file': uploaded_pdf,
                'title': 'Test Resume PDF'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("File uploaded successfully!" in str(m) for m in messages))

    def test_upload_invalid_filetype(self):
        self.client.login(username='testuser', password='testpass')
        txt_file = SimpleUploadedFile("test.txt", b"Just some text", content_type="text/plain")
        
        response = self.client.post(
            reverse('upload_file'),
            {
                'file': txt_file,
                'title': 'Test Invalid File' 
            },
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Invalid filetype" in str(m) for m in messages))


class UploadedJobListingViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

def test_post_valid_text(self):
    self.client.login(username='testuser', password='testpass')
    response = self.client.post(
        reverse('save_pasted_text'),
        {'paste-text': 'This is a pasted test.', 'title': 'Test Title'},
        follow=True 
    )

    self.assertEqual(response.status_code, 200)
    messages_list = list(messages.get_messages(response.wsgi_request))
    self.assertTrue(any("Text uploaded successfully!" in str(m) for m in messages_list))


    def test_post_empty_text(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('save_pasted_text'), {'paste-text': ''}, follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any("Text field cannot be empty" in str(m) for m in messages_list))


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ResumeUploadTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.resume = UploadedResume.objects.create(user=self.user, content='Sample Resume Content', title='My Resume')
        self.other_resume = UploadedResume.objects.create(user=self.other_user, content='Not Yours', title='Other Resume')

    def test_delete_resume_post_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('delete_resume', args=[self.resume.id]))
        self.assertRedirects(response, reverse('profile'))
        with self.assertRaises(UploadedResume.DoesNotExist):
            UploadedResume.objects.get(id=self.resume.id)

    def test_delete_resume_get_does_not_delete(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('delete_resume', args=[self.resume.id]))
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(UploadedResume.objects.filter(id=self.resume.id).exists())

    def test_cannot_delete_other_users_resume(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('delete_resume', args=[self.other_resume.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(UploadedResume.objects.filter(id=self.other_resume.id).exists())

class ResumeDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.resume = UploadedResume.objects.create(
            user=self.user,
            title='Sample Resume',
            content='This is the resume content.'
        )

    def test_resume_detail_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('resume_detail', args=[self.resume.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resume_detail.html')
        self.assertEqual(response.context['resume'], self.resume)

    def test_resume_detail_view_unauthenticated_redirects(self):
        response = self.client.get(reverse('resume_detail', args=[self.resume.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_resume_detail_view_nonexistent_resume(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('resume_detail', args=[999]))
        self.assertEqual(response.status_code, 404)


class UploadedJobListingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.url = "/pasted-text/"


    def tearDown(self):
        # Clean up the created pasted_texts directory after test
        user_dir = os.path.join(settings.MEDIA_ROOT, 'pasted_texts', str(self.user.id))
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir)

    def test_valid_job_listing_paste_upload(self):
        
        data = {
            "paste-text": "This is a job listing description.",
            "title": "Cool Job"
        }


        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertTrue(any("Text uploaded successfully!" in str(m) for m in messages))
        expected_dir = os.path.join(settings.MEDIA_ROOT, 'pasted_texts', str(self.user.id))
        self.assertTrue(os.path.exists(expected_dir))

        # Check that an UploadedJobListing was created
        from active_interview_app.models import UploadedJobListing
        self.assertEqual(UploadedJobListing.objects.count(), 1)
        job = UploadedJobListing.objects.first()
        self.assertEqual(job.title, "Cool Job")
        self.assertEqual(job.user, self.user)


class UploadedResumeViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = APIClient()
        self.client.login(username="testuser", password="password")
        self.url = reverse('upload_file')

    def test_valid_resume_upload(self):
        with open('test.pdf', 'rb') as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, 302)

    def test_invalid_resume_upload(self):
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UploadedResume.objects.count(), 0)

# Tests to be implemented at a later date.

#class UploadedResumeListTests(unittest.TestCase):
#    def setUp(self):
#        self.client = APIClient()
#        self.user = User.objects.create_user(username="testuser", password="testpass")
#        self.client.login(username="testuser", password="testpass")
#
#    def test_get_uploaded_file_list(self):
#        # Create an uploaded file for the user
#        UploadedResume.objects.create(user=self.user, file="testfile.txt")
#
#        # Send GET request to list uploaded files
#        response = self.client.get(reverse('uploaded_file_list'))
#
#       # Ensure status code is 200
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        # Ensure the file is in the response data
#        self.assertEqual(len(response.data), 1)
#        self.assertEqual(response.data[0]['file'], 'testfile.txt')


#class UploadedResumeDetailTests(unittest.TestCase):
#    def setUp(self):
#        self.client = APIClient()
#        self.user = User.objects.create_user(username="testuser", password="testpass")
#        self.client.login(username="testuser", password="testpass")
#        self.uploaded_file = UploadedResume.objects.create(user=self.user, file="testfile.txt")

    #Feature that shows users uploaded file details not ready yet. Test commented out for the time being.
    #def test_get_uploaded_file(self):
    #    response = self.client.get(reverse('uploaded_file_detail', kwargs={'pk': self.uploaded_file.pk}))
    #    self.assertEqual(response.status_code, status.HTTP_200_OK)
    #    self.assertEqual(response.data['file'], 'testfile.txt')


#class UploadedJobListingListTests(unittest.TestCase):
#    def setUp(self):
#        self.client = APIClient()
#        self.user = User.objects.create_user(username="testuser", password="testpass")
#        self.client.login(username="testuser", password="testpass")
#
#    def test_get_pasted_text_list(self):
#        # Create a pasted text entry
#        UploadedJobListing.objects.create(user=self.user, content="Test paste")
#
#        # Send GET request to list pasted texts
#        response = self.client.get(reverse('pasted_text_list'))
#
#        # Ensure status code is 200
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        # Ensure the pasted text is in the response data
#        self.assertEqual(len(response.data), 1)
#        self.assertEqual(response.data[0]['content'], 'Test paste')


#class UploadedJobListingDetailTests(unittest.TestCase):
#    def setUp(self):
#        self.client = APIClient()
#        self.user = User.objects.create_user(username="testuser", password="testpass")
#        self.client.login(username="testuser", password="testpass")
#        self.pasted_text = UploadedJobListing.objects.create(user=self.user, content="Test paste")

#    def test_get_pasted_text(self):
#        response = self.client.get(reverse('pasted_text_detail', kwargs={'pk': self.pasted_text.pk}))
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertEqual(response.data['content'], 'Test paste')


#class UploadedResumeListTests(TestCase):
#    def setUp(self):
#        self.client = Client()
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.client.login(username='testuser', password='testpass')

#    def test_get_uploaded_file_list(self):
#        # Create a file entry for the user
#        uploaded_file = UploadedFile.objects.create(user=self.user, file='testfile.pdf')

#        response = self.client.get(reverse('uploaded_file_list'))

#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, uploaded_file.file.name)

#    def test_post_uploaded_file(self):
#        with open('testfile.pdf', 'wb') as f:
#            f.write(b"PDF content")
#        with open('testfile.pdf', 'rb') as f:
#            response = self.client.post(reverse('uploaded_file_list'), {'file': f}, follow=True)

#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(UploadedFile.objects.count(), 1)
#        uploaded_file = UploadedFile.objects.first()
#        self.assertEqual(uploaded_file.file.name, 'testfile.pdf')


#class UploadedFileDetailTests(TestCase):
#    def setUp(self):
#        self.client = Client()
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.client.login(username='testuser', password='testpass')
#        self.uploaded_file = UploadedFile.objects.create(user=self.user, file='testfile.pdf')

    #Feature that shows users uploaded file details not ready yet. Test commented out for the time being.
    #def test_get_uploaded_file_detail(self):
    #    response = self.client.get(reverse('uploaded_file_detail', kwargs={'pk': self.uploaded_file.pk}))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertContains(response, self.uploaded_file.file.name)

    #def test_put_uploaded_file(self):
    #    response = self.client.put(reverse('uploaded_file_detail', kwargs={'pk': self.uploaded_file.pk}),
    #                               {'file': 'newfile.pdf'}, follow=True)
    #    self.assertEqual(response.status_code, 200)
    #    self.uploaded_file.refresh_from_db()
    #    self.assertEqual(self.uploaded_file.file.name, 'newfile.pdf')

    #def test_delete_uploaded_file(self):
    #    response = self.client.delete(reverse('uploaded_file_detail', kwargs={'pk': self.uploaded_file.pk}))
    #    self.assertEqual(response.status_code, 204)
    #    self.assertEqual(UploadedFile.objects.count(), 0)


#class UploadedJobListingListTests(TestCase):
#    def setUp(self):
#        self.client = Client()
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.client.login(username='testuser', password='testpass')

    #Feature that shows users paste text list not ready yet. Test commented out for the time being.
    #def test_get_pasted_text_list(self):
    #    pasted_text = UploadedJobListing.objects.create(user=self.user, content='Test paste')

    #    response = self.client.get(reverse('pasted_text_list'))

    #    self.assertEqual(response.status_code, 200)
    #    self.assertContains(response, pasted_text.content)

    #def test_post_pasted_text(self):
    #    response = self.client.post(reverse('pasted_text_list'), {'content': 'Another test paste'}, follow=True)

    #    self.assertEqual(response.status_code, 200)
    #    self.assertEqual(UploadedJobListing.objects.count(), 1)
    #    pasted_text = UploadedJobListing.objects.first()
    #    self.assertEqual(pasted_text.content, 'Another test paste')


#class UploadedJobListingDetailTests(TestCase):
#    def setUp(self):
#        self.client = Client()
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.client.login(username='testuser', password='testpass')
#        self.pasted_text = UploadedJobListing.objects.create(user=self.user, content='Test paste')

#    def test_get_pasted_text_detail(self):
#        response = self.client.get(reverse('pasted_text_detail', kwargs={'pk': self.pasted_text.pk}))
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, self.pasted_text.content)
    #Feature that shows users uploaded file details not ready yet. Test commented out for the time being.
#    def test_put_pasted_text(self):
#        response = self.client.put(reverse('pasted_text_detail', kwargs={'pk': self.pasted_text.pk}),
#                                   {'content': 'Updated paste'}, follow=True)
#        self.assertEqual(response.status_code, 200)
#        self.pasted_text.refresh_from_db()
#        self.assertEqual(self.pasted_text.content, 'Updated paste')

#    def test_delete_pasted_text(self):
#        response = self.client.delete(reverse('pasted_text_detail', kwargs={'pk': self.pasted_text.pk}))
#        self.assertEqual(response.status_code, 204)
#        self.assertEqual(UploadedJobListing.objects.count(), 0)