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
from unittest.mock import patch
from django.conf import settings
from docx import Document as DocxDocument
import os
import markdown
import unittest
import shutil


#Run using python3 manage.py test active_interview_app.tests.test_upload

class ResumeUploadTestCase(TestCase):
    def test_file_upload(self):
        test_file = SimpleUploadedFile(
            "testfile.txt", b"This is the content of the file.",
            content_type="text/plain")
        response = self.client.post(reverse('upload_file'), {
                                    'file': test_file}, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UploadedResume.objects.count(), 1)
        uploaded_file = UploadedResume.objects.first()
        self.assertEqual(uploaded_file.file.name, "uploads/testfile.txt")

    @patch("filetype.guess")
    def test_invalid_file_type_upload(self, mock_guess):
        mock_guess.return_value = type(
            "obj", (object,), {"extension": "exe"})  # Not allowed

        file = SimpleUploadedFile(
            "malware.exe", b"MZ fake exe",
            content_type="application/octet-stream")
        response = self.client.post(reverse("upload_file"), {
            "file": file,
            "title": "Hacked"
        }, follow=True)

        self.assertContains(
            response, "Invalid filetype. Only PDF and DOCX files are allowed.")

    @patch("filetype.guess")
    @patch("pymupdf4llm.to_markdown", side_effect=Exception("Boom!"))
    def test_exception_during_processing(self, mock_to_markdown, mock_guess):
        mock_guess.return_value = type("obj", (object,), {"extension": "pdf"})

        file = SimpleUploadedFile(
            "test.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        response = self.client.post(reverse("upload_file"), {
            "file": file,
            "title": "Exploding Resume"
        }, follow=True)

        self.assertContains(response, "Error processing the file: Boom!")

    def test_invalid_form_submission(self):
    # Missing file field entirely
        response = self.client.post(reverse("upload_file"), {
            "title": "Missing file"
        }, follow=True)

        self.assertContains(response, "There was an issue with the form.")

    def test_get_request_renders_upload_form(self):
        response = self.client.get(reverse("upload_file"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/document-list.html")

    @patch("filetype.guess")
    def test_valid_docx_upload(self, mock_guess):
        # Create a DOCX file in memory
        doc = DocxDocument()
        doc.add_paragraph("This is a test paragraph.")
        fake_file = BytesIO()
        doc.save(fake_file)
        fake_file.seek(0)

        # Simulate filetype as 'docx'
        mock_guess.return_value = type("obj", (object,), {"extension": "docx"})

        uploaded = SimpleUploadedFile("resume.docx", fake_file.read(),
                                      content_type="application/vnd.openxmlfor\
                                        mats-officedocument.wordprocessingml.d\
                                        ocument")
        response = self.client.post(reverse("upload_file"), {
            "file": uploaded,
            "title": "Test DOCX"
        }, follow=True)

        # Check for successful upload
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "File uploaded successfully!")
        self.assertEqual(UploadedResume.objects.count(), 1)

        # Check content was saved as markdown
        saved = UploadedResume.objects.first()
        self.assertIn(markdown.markdown(
            "This is a test paragraph."), saved.content)


class UploadedJobListingUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")


def test_pasted_text_upload(self):
    response = self.client.post(reverse('save_pasted_text'), {
        'paste-text': 'This is a test paste.',
        'title': 'Sample Title'
    }, follow=True)

    self.assertEqual(response.status_code, 200)

    messages_list = list(messages.get_messages(response.wsgi_request))
    self.assertTrue(any("Text uploaded successfully!" in str(m)
                    for m in messages_list))
    pasted = UploadedJobListing.objects.first()
    self.assertEqual(pasted.content, 'This is a test paste.')
    self.assertEqual(pasted.user, self.user)

    def test_pasted_text_upload_blank(self):
        response = self.client.post(reverse('save_pasted_text'), {
            'paste-text': ''
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(UploadedJobListing.objects.count(), 0)


class ResumeUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

    def test_upload_valid_pdf(self):
        print(f"Current working directory: {os.getcwd()}")
        pdf_path = os.path.join(
            os.getcwd(), 'active_interview_app', 'tests', 'test.pdf')

        self.assertTrue(os.path.exists(pdf_path),
                        f"Test PDF file not found at {pdf_path}")

        with open(pdf_path, 'rb') as pdf_file:
            uploaded_pdf = SimpleUploadedFile(
                'test.pdf', pdf_file.read(), content_type='application/pdf')

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
        self.assertTrue(any("File uploaded successfully!" in str(m)
                        for m in messages))

    def test_upload_invalid_filetype(self):
        self.client.login(username='testuser', password='testpass')
        txt_file = SimpleUploadedFile(
            "test.txt", b"Just some text", content_type="text/plain")

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
        self.user = User.objects.create_user(
            username='testuser', password='testpass')


def test_post_valid_text(self):
    self.client.login(username='testuser', password='testpass')
    response = self.client.post(
        reverse('save_pasted_text'),
        {'paste-text': 'This is a pasted test.', 'title': 'Test Title'},
        follow=True
    )

    self.assertEqual(response.status_code, 200)
    messages_list = list(messages.get_messages(response.wsgi_request))
    self.assertTrue(any("Text uploaded successfully!" in str(m)
                    for m in messages_list))

    def test_post_empty_text(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('save_pasted_text'), {
                                    'paste-text': ''}, follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any("Text field cannot be empty" in str(m)
                        for m in messages_list))


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ResumeUploadTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.other_user = User.objects.create_user(
            username='otheruser', password='password')
        self.resume = UploadedResume.objects.create(
            user=self.user, content='Sample Resume Content', title='My Resume')
        self.other_resume = UploadedResume.objects.create(
            user=self.other_user, content='Not Yours', title='Other Resume')

    def test_delete_resume_post_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(
            reverse('delete_resume', args=[self.resume.id]))
        self.assertRedirects(response, reverse('profile'))
        with self.assertRaises(UploadedResume.DoesNotExist):
            UploadedResume.objects.get(id=self.resume.id)

    def test_delete_resume_get_does_not_delete(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('delete_resume', args=[self.resume.id]))
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(UploadedResume.objects.filter(
            id=self.resume.id).exists())

    def test_cannot_delete_other_users_resume(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(
            reverse('delete_resume', args=[self.other_resume.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(UploadedResume.objects.filter(
            id=self.other_resume.id).exists())


class ResumeDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.resume = UploadedResume.objects.create(
            user=self.user,
            title='Sample Resume',
            content='This is the resume content.'
        )

    def test_resume_detail_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('resume_detail', args=[self.resume.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/resume_detail.html')
        self.assertEqual(response.context['resume'], self.resume)

    def test_resume_detail_view_unauthenticated_redirects(self):
        response = self.client.get(
            reverse('resume_detail', args=[self.resume.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_resume_detail_view_nonexistent_resume(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('resume_detail', args=[999]))
        self.assertEqual(response.status_code, 404)


class UploadedJobListingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.url = "/pasted-text/"

    def tearDown(self):
        user_dir = os.path.join(settings.MEDIA_ROOT,
                                'pasted_texts', str(self.user.id))
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
        self.assertTrue(any("Text uploaded successfully!" in str(m)
                        for m in messages))
        expected_dir = os.path.join(
            settings.MEDIA_ROOT, 'pasted_texts', str(self.user.id))
        self.assertTrue(os.path.exists(expected_dir))

        from active_interview_app.models import UploadedJobListing
        self.assertEqual(UploadedJobListing.objects.count(), 1)
        job = UploadedJobListing.objects.first()
        self.assertEqual(job.title, "Cool Job")
        self.assertEqual(job.user, self.user)


class UploadedResumeViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.client = APIClient()
        self.client.login(username="testuser", password="password")
        self.url = reverse('upload_file')

    def test_valid_resume_upload(self):
        with open('test.pdf', 'rb') as file:
            response = self.client.post(
                self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, 302)

    def test_invalid_resume_upload(self):
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UploadedResume.objects.count(), 0)


class FileUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    @patch("filetype.guess")
    def test_file_type_guess_called_on_upload(self, mock_guess):
        mock_guess.return_value = type("obj", (object,), {"extension": "pdf"})

        sample_file = SimpleUploadedFile(
            "test.pdf",
            b"%PDF-1.4 test content",
            content_type="application/pdf"
        )

        response = self.client.post(reverse("upload_file"), {
            "file": sample_file,
            "title": "Test Resume"
        })

        self.assertEqual(response.status_code, 302)
        mock_guess.assert_called_once()


class EditResumeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.resume = UploadedResume.objects.create(
            user=self.user,
            title='Old Title',
            original_filename='resume.docx',
            filesize=1234,
            content='Old content',
        )

    def test_get_edit_resume_page(self):
        url = reverse('edit_resume', args=[self.resume.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/edit_document.html')
        self.assertContains(response, 'Old Title')

    def test_post_valid_edit_resume_form(self):
        url = reverse('edit_resume', args=[self.resume.id])
        response = self.client.post(url, {
            'title': 'Updated Title',
            'content': 'Updated content',
        })

        self.assertRedirects(response, reverse(
            'resume_detail', args=[self.resume.id]))

        self.resume.refresh_from_db()
        self.assertEqual(self.resume.title, 'Updated Title')
        self.assertEqual(self.resume.content, 'Updated content')

    def test_post_invalid_edit_resume_form(self):
        url = reverse('edit_resume', args=[self.resume.id])
        response = self.client.post(url, {
            'title': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/edit_document.html')
        self.assertFormError(response, 'form', 'title',
                             'This field is required.')


class EditJobPostingViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='employer', password='securepass')
        self.client.login(username='employer', password='securepass')

        self.job = UploadedJobListing.objects.create(
            user=self.user,
            title='Junior Developer',
            content='Looking for a passionate developer.',
        )

    def test_get_edit_job_posting_page(self):
        url = reverse('edit_job_posting', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/edit_job_posting.html')
        self.assertContains(response, 'Junior Developer')

    def test_post_valid_job_edit(self):
        url = reverse('edit_job_posting', args=[self.job.id])
        response = self.client.post(url, {
            'title': 'Senior Developer',
            'content': 'Now hiring a senior dev.',
        })

        self.assertRedirects(response, reverse(
            'job_posting_detail', args=[self.job.id]))

        self.job.refresh_from_db()
        self.assertEqual(self.job.title, 'Senior Developer')
        self.assertEqual(self.job.content, 'Now hiring a senior dev.')