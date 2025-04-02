from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import Chat


# === Helper Fucntions ===
def generateExampleUser():
    user = User.objects.create(
        username="example", 
        password="goodray31"
    )

    return user

def generateExampleChat():
    chat = Chat.objects.create(
        title="Example Title",
        owner=generateExampleUser(),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Generate 7 random numbers"},
            {"role": "assistant", "content": "Sure, here are 7 randomly generated numbers:\n\n1. 34\n2. 12\n3. 78\n4. 56\n5. 23\n6. 89\n7. 45\n\nPlease let me know if you need more numbers or if you have any specific range in mind!"},
            {"role": "user", "content": "Please sum those numbers"},
            {"role": "assistant", "content": "Certainly! Let's sum the numbers:\n\n34 + 12 + 78 + 56 + 23 + 89 + 45 = 337\n\nThe total sum is 337."}
        ]
    )

    return chat


# === Model Tests ===
class TestChatModel(TestCase):
    def setUp(self):
        self.chat = generateExampleChat()

    def testStr(self):
        self.assertEqual(self.chat.__str__(), "Example Title")
