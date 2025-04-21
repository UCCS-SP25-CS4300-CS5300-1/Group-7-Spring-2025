from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

# from ..forms import CreateChatForm, EditChatForm
from ..models import Chat, UploadedJobListing, UploadedResume


# === Helper Fucntions ===
def generateExampleUser():
    user = User.objects.create_user(
        username="example",
        password="goodray31"
    )

    return user

# def generateOtherUser():
#     user = User.objects.create_user(
#         username="other",
#         password="firstforce61"
#     )

#     return user


def generateExampleChat(owner):
    chat = Chat.objects.create(
        title="Example Title",
        owner=owner,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Generate 7 random numbers"},
            {
                "role": "assistant",
                "content": "Sure, here are 7 randomly generated numbers:\n\n1.\
                        34\n2. 12\n3. 78\n4. 56\n5. 23\n6. 89\n7. 45\n\nPlease\
                        let me know if you need more numbers or if you have\
                        any specific range in mind!"
            },
            {"role": "user", "content": "Please sum those numbers"},
            {
                "role": "assistant",
                "content": "Certainly! Let's sum the numbers:\n\n34 + 12 + 78 \
                    + 56 + 23 + 89 + 45 = 337\n\nThe total sum is 337."
            }
        ]
    )

    return chat


def generateExampleJobListing(user):
    job_listing = UploadedJobListing.objects.create(
        user=user,
        title="Example Listing",
        content="# Example Content\n\nmwahahaha"
    )

    return job_listing


def generateExampleResume(user):
    resume = UploadedResume.objects.create(
        user=user,
        title="Example Resume",
        content="# Example Content 2\n\nnononono"
    )

    return resume


# === Model Tests ===
class TestChatModel(TestCase):
    def setUp(self):
        self.user = generateExampleUser()
        self.chat = generateExampleChat(self.user)

    def testChatModelStr(self):
        self.assertEqual(self.chat.__str__(), "Example Title")


# === View Tests ===
class TestChatListView(TestCase):
    def setUp(self):
        self.user = generateExampleUser()
        self.chat = generateExampleChat(self.user)
        self.client.force_login(self.user)

    def testChatList(self):
        # Call the view with a response
        response = self.client.get(reverse('chat-list'))

        # Validate that the view is valid
        self.assertEqual(response.status_code, 200)

        # Validate that the index template was used
        self.assertTemplateUsed(response, 'base-sidebar.html')


class TestCreateChatView(TestCase):
    def setUp(self):
        self.user = generateExampleUser()
        self.chat = generateExampleChat(self.user)
        self.client.force_login(self.user)

    def testGETCreateChatView(self):
        # Call the view with a response
        response = self.client.get(reverse('chat-create'))

        # Validate that the view is valid
        self.assertEqual(response.status_code, 200)

        # Validate that the index template was used
        self.assertTemplateUsed(response, 'base-sidebar.html')

    def testPOSTCreateChatView(self):
        # Call the view with a response
        response = self.client.post(reverse('chat-create'),
            {
                "title": "Example Title Strikes Back",
                "type": Chat.GENERAL,
                "difficulty": 5,
                "listing_choice": generateExampleJobListing(self.user).id,
                "resume_choice": generateExampleResume(self.user).id,
                "create": "create"
            }
        )

        # Validate that the view is valid.  This view redirects
        self.assertEqual(response.status_code, 302)

        # Validate that the new chat has been created
        self.assertTrue(Chat.objects.filter(
            title='Example Title Strikes Back').exists())


class TestChatView(TestCase):
    def setUp(self):
        self.user = generateExampleUser()
        self.chat = generateExampleChat(self.user)
        self.client.force_login(self.user)

    def testGETChatView(self):
        # Call the view with a response
        response = self.client.get(reverse('chat-view', args=[self.chat.id]))

        # Validate that the view is valid
        self.assertEqual(response.status_code, 200)

        # Validate that the index template was used
        self.assertTemplateUsed(response, 'base-sidebar.html')

    def testPOSTChatView(self):
        # Call view with an ai prompt
        response = self.client.post(reverse('chat-view', args=[self.chat.id]),
            {
                "message": "What is pi?"
            }
        )

        # Validate that the view is valid.  This view redirects
        self.assertEqual(response.status_code, 200)

        # Check the ai response for a valid response
        print(response.content.decode('utf-8'))
        self.assertIn("3.14", response.content.decode('utf-8'))


class TestEditChatView(TestCase):
    def setUp(self):
        self.user = generateExampleUser()
        self.chat = generateExampleChat(self.user)
        self.client.force_login(self.user)

    def testGETEditChatView(self):
        # Call the view with a response
        response = self.client.get(reverse('chat-edit', args=[self.chat.id]))

        # Validate that the view is valid
        self.assertEqual(response.status_code, 200)

        # Validate that the index template was used
        self.assertTemplateUsed(response, 'base-sidebar.html')

    def testPOSTEditChatView(self):
        # Call the view to update the current item's title
        response = self.client.post(reverse('chat-edit', args=[self.chat.id]),
            {
                "title": "Changed Title",
                "difficulty": 3,
                "update": "update"
            }
        )

        # Validate that the view is valid.  This view redirects
        self.assertEqual(response.status_code, 302)

        # Validate that the chat's title has been updated
        self.assertEqual(Chat.objects.get(id=self.chat.id).title,
                         "Changed Title")
        self.assertEqual(Chat.objects.get(id=self.chat.id).difficulty, 3)


class TestDeleteChatView(TestCase):
    def setUp(self):
        self.user = generateExampleUser()
        self.chat = generateExampleChat(self.user)
        self.client.force_login(self.user)

    def testPOSTDeleteChatView(self):
        # Call the view to update the current item's title
        response = self.client.post(reverse('chat-delete',
                                            args=[self.chat.id]),
            {
                "delete": "delete"
            }
        )

        # Validate that the view is valid.  This view redirects
        self.assertEqual(response.status_code, 302)

        # Validate that the chat has been deleted
        self.assertFalse(Chat.objects.filter(id=self.chat.id).exists())
