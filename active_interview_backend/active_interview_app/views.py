import os
import filetype
from openai import OpenAI
import pymupdf4llm
import markdown

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .forms import *
from .models import *
from .serializers import *


allowed_types = ['pdf']


# Init openai client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# Create your views here.
def index(request):
    return render(request, 'index.html')

# def demo(request):
#     return render(request, os.path.join('demo', 'demo.html'))

def features(request):
    return render(request, 'features.html')

def features(request):
    return render(request, 'features.html')


# @login_required
# def chat_view(request):
#     if request.method == 'GET':
#         chat = Chat.objects.create(
#             owner=request.user,
#             title="New Chat",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#             ]
#         )

#         owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')

#         request.session['chat_id'] = chat.id

#         context = {}
#         context['chat'] = chat
#         context['owner_chats'] = owner_chats

#         return render(request, os.path.join('chat', 'chat-view.html'), context)
    
#     elif request.method == 'POST':
#         chat_id = request.session.get('chat_id')
#         chat = Chat.objects.get(id=chat_id)

#         user_message = request.POST.get('message', '')

#         new_messages = chat.messages
#         new_messages.append({"role": "user", "content": user_message})

#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=new_messages,
#             max_tokens=500
#         )
#         ai_message = response.choices[0].message.content
#         new_messages.append({"role": "assistant", "content": ai_message})

#         chat.messages = new_messages
#         chat.save()

#         return JsonResponse({'message': ai_message})


@login_required
def chat_list(request):
    owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')

    context = {}
    context['owner_chats'] = owner_chats

    return render(request, os.path.join('chat', 'chat-list.html'), context)


class CreateChat(LoginRequiredMixin, View):
    def get(self, request):
        owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')
        
        form = ChatForm()

        context = {}
        context['owner_chats'] = owner_chats
        context['form'] = form

        return render(request, os.path.join('chat', 'chat-create.html'), context)

    def post(self, request):
        if 'create' in request.POST:
            form = ChatForm(request.POST)
            
            if form.is_valid():
                chat = form.save(commit=False)

                chat.owner = request.user
                chat.messages = [
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant."
                    },
                ]

                # Get the job listing and resume from the form 
                job_listing_id = request.POST.get('job_listing')  # Assuming the form includes this field
                resume_id = request.POST.get('resume')  # Assuming the form includes this field

                # If a job listing is selected, set the foreign key
                if job_listing_id:
                    try:
                        job_listing = UploadedJobListing.objects.get(id=job_listing_id)
                        chat.job_listing = job_listing
                    except UploadedJobListing.DoesNotExist:
                        # Handle case where the job listing doesn't exist
                        pass

                # If a resume is selected, set the foreign key
                if resume_id:
                    try:
                        resume = UploadedResume.objects.get(id=resume_id)
                        chat.resume = resume
                    except UploadedResume.DoesNotExist:
                        # Handle case where the resume doesn't exist
                        pass                

                chat.save()

                return redirect("chat-view", chat_id=chat.id)


class ChatView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # manually grab chat id from kwargs and process it
        chat = Chat.objects.get(id=self.kwargs['chat_id'])

        return self.request.user == chat.owner

    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')

        context = {}
        context['chat'] = chat
        context['owner_chats'] = owner_chats

        return render(request, os.path.join('chat', 'chat-view.html'), context)

    def post(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        user_message = request.POST.get('message', '')

        new_messages = chat.messages
        new_messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=new_messages,
            max_tokens=500
        )
        ai_message = response.choices[0].message.content
        new_messages.append({"role": "assistant", "content": ai_message})

        chat.messages = new_messages
        chat.save()

        return JsonResponse({'message': ai_message})


class EditChat(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # manually grab chat id from kwargs and process it
        chat = Chat.objects.get(id=self.kwargs['chat_id'])

        return self.request.user == chat.owner
        
    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        owner_chats = Chat.objects.filter(owner=request.user).order_by('-modified_date')
        
        form = ChatForm(initial=model_to_dict(chat), instance=chat)

        context = {}
        context['chat'] = chat
        context['owner_chats'] = owner_chats
        context['form'] = form

        return render(request, os.path.join('chat', 'chat-edit.html'), context)

    def post(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        if 'update' in request.POST:
            form = ChatForm(request.POST, instance=chat)
            
            if form.is_valid():
                chat = form.save(commit=False)

                # Do other stuff if necessary, especially if a file is changed

                chat.save()

                return redirect("chat-view", chat_id=chat.id)


# Note: this class has no template.  it is technically built into base-sidebar
class DeleteChat(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # manually grab chat id from kwargs and process it
        chat = Chat.objects.get(id=self.kwargs['chat_id'])

        return self.request.user == chat.owner
        
    def post(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        if 'delete' in request.POST:
            chat.delete()
            return redirect("chat-list")
        # else:
        #     print("delete not in form")
        #     return redirect("chat-view", chat_id=chat.id)

@login_required
def loggedin(request):
    return render(request, 'loggedinindex.html')


def register(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        group = Group.objects.get(name='average_role')
        user.groups.add(group)
        #user = User.objects.create(user=user)
        user.save()
        messages.success(request, 'Account was created for ' + username)
        return redirect('/accounts/login/?next=/')
    context={'form':form}
        
    return render(request, 'registration/register.html', context)


# === Joel's file upload views ===


@login_required
def upload_file(request):
    print("POST request received")
    if request.method == "POST":
        print("method qualifies as post.")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid.")
            uploaded_file = request.FILES["file"]
            file_name = uploaded_file.name

            file_type = filetype.guess(uploaded_file.read())
            uploaded_file.seek(0)

            allowed_types = ['pdf', 'docx', 'txt']  # Define allowed file types (for example)

            if file_type and file_type.extension in allowed_types:
                print("it's in allow types,")
                # Create instance but don't commit to the database yet
                instance = form.save(commit=False)
                instance.user = request.user
                instance.original_filename = file_name
                instance.filesize = uploaded_file.size
                instance.save()

                # Optionally convert the file to markdown if needed
                uploaded_file_url = os.path.join(settings.MEDIA_URL, file_name)
                markdown_text = pymupdf4llm.to_markdown(uploaded_file)

                # Show success message and redirect
                messages.success(request, "File uploaded successfully!")
                return render(request, 'documents/document-list.html', {'markdown_text': markdown_text})  # Redirect to document list page after successful upload
            else:
                messages.error(request, "Invalid filetype.")
        else:
            messages.error(request, "There was an issue with the form.")
    else:
        form = UploadFileForm()

    return render(request, "documents/document-list.html", {"form": form})



class UploadedJobListingView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the text from the request
        text = request.POST.get("paste-text", '').strip()
        print(request.POST)


        # Check if the text is empty
        if not text:
            messages.error(request, "Text field cannot be empty.")
            return redirect('document-list')


        user = request.user
        timestamp = now().strftime("%d%m%Y_%H%M%S")
        filename = f"{user.username}_{timestamp}.txt"

        # Create a directory for the user to store pasted text files
        user_dir = os.path.join(settings.MEDIA_ROOT, 'pasted_texts', str(user.id))
        os.makedirs(user_dir, exist_ok=True)
        filepath = os.path.join(user_dir, filename)

        # Convert the text to Markdown
        markdown_text = markdown.markdown(text)

        # Save the text content to a file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

        # Create and save the UploadedJobListing object in the database
        job_listing = UploadedJobListing(user=user, content=text, filepath=filepath)
        job_listing.save()


        # Show success message and render the converted markdown
        messages.success(request, "Text uploaded successfully!")
        return render(request, 'documents/document-list.html', {'markdown_text': markdown_text})



class UploadedResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        files = UploadedResume.objects.filter(user=request.user)
        serializer = UploadedResumeSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UploadedResumeSerializer(data=request.data)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



#probably relative file path, which is causing the error
class UploadedResumeDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        file = UploadedResume.objects.get(pk=pk, user=request.user)


        serializer = UploadedResumeSerializer(file)
        return Response(serializer.data)

    def put(self, request, pk):
        file = UploadedResume.objects.get(pk=pk, user=request.user)


        serializer = UploadedResumeSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        file = UploadedResume.objects.get(pk=pk, user=request.user)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobListingList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # List all pasted text entries for the authenticated user
        texts = UploadedJobListing.objects.filter(user=request.user)
        serializer = UploadedJobListingSerializer(texts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new pasted text entry
        serializer = UploadedJobListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListingDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Retrieve a specific pasted text entry by id
        text = UploadedJobListing.objects.get(pk=pk, user=request.user)


        serializer = UploadedJobListingSerializer(text)
        return Response(serializer.data)

    def put(self, request, pk):
        # Update a specific pasted text entry by id
        text = UploadedJobListing.objects.get(pk=pk, user=request.user)


        serializer = UploadedJobListingSerializer(text, data=request.data, partial=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        # Delete a specific pasted text entry by id
        text = PUploadedJobListing.objects.get(pk=pk, user=request.user)

        text.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DocumentList(View):
    def get(self, request):
        return render(request, 'documents/document-list.html')