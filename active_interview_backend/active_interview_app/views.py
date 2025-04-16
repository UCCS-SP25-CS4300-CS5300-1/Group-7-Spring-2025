import os
import filetype
from openai import OpenAI
import pymupdf4llm
import textwrap
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





# Init openai client
client = OpenAI(api_key=settings.OPENAI_API_KEY)
MAX_TOKENS = 15000


# Create your views here.
def index(request):
    return render(request, 'index.html')

def aboutus(request):
    return render(request, 'about-us.html')

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
        
        form = CreateChatForm(user=request.user) # Pass user into chatform

        context = {}
        context['owner_chats'] = owner_chats
        context['form'] = form

        return render(request, os.path.join('chat', 'chat-create.html'), context)

    def post(self, request):
        if 'create' in request.POST:
            form = CreateChatForm(request.POST, user=request.user)
            
            if form.is_valid():
                chat = form.save(commit=False)

                chat.job_listing = form.cleaned_data['listing_choice']
                chat.resume = form.cleaned_data.get('resume_choice')
                chat.owner = request.user

                # Prompts are edited by ChatGPT after being written by a human developer
                system_prompt = "An error has occurred.  Please notify the user about this." # Default message.  Should only show up if something went wrong.
                if chat.resume: # if resume is present
                    system_prompt = textwrap.dedent("""\
                        You are a professional interviewer for a company preparing for a candidate’s interview.
                        You will act as the interviewer and engage in a roleplaying session with the candidate.
                        
                        Please review the job listing and resume below:
                        
                        # Job Listing:
                        \"\"\"{listing}\"\"\"
                        
                        # Candidate Resume:
                        \"\"\"{resume}\"\"\"
                        
                        Ignore any formatting issues in the resume, and focus on its content. 
                        Begin the session by greeting the candidate and asking an introductory question about their background, 
                        then move on to deeper, role-related questions based on the job listing and resume.
                    """).format(listing=chat.job_listing.content, resume=chat.resume.content)
                else: # if no resume
                    system_prompt = textwrap.dedent("""\
                        You are a professional interviewer for a company preparing for a candidate’s interview.
                        You will act as the interviewer and engage in a roleplaying session with the candidate.
                        
                        Please review the job listing below:
                        
                        # Job Listing:
                        \"\"\"{listing}\"\"\"
                        
                        Begin the session by greeting the candidate and asking an introductory question about their background, 
                        then move on to role-specific questions based on the job listing.
                    """).format(listing=chat.job_listing.content)


                chat.messages = [
                    {
                        "role": "system", 
                        "content": system_prompt
                    },
                ]

                # Make ai speak first
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=chat.messages,
                    max_tokens=MAX_TOKENS
                )
                ai_message = response.choices[0].message.content
                chat.messages.append({"role": "assistant", "content": ai_message})

                chat.save()

                return redirect("chat-view", chat_id=chat.id)
            # else:
            #     print("chat form invalid")


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
            max_tokens=MAX_TOKENS
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
        
        form = EditChatForm(initial=model_to_dict(chat), instance=chat)

        context = {}
        context['chat'] = chat
        context['owner_chats'] = owner_chats
        context['form'] = form

        return render(request, os.path.join('chat', 'chat-edit.html'), context)

    def post(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        if 'update' in request.POST:
            form = EditChatForm(request.POST, instance=chat)
            
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


@login_required
def profile(request):
    resumes = UploadedResume.objects.filter(user = request.user)
    job_listings = UploadedJobListing.objects.filter(user = request.user)
    return render(request, 'profile.html', {'resumes':resumes, 'job_listings':job_listings})


# === Joel's file upload views ===


@login_required
def upload_file(request):
    allowed_types = ['pdf']

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            file_name = uploaded_file.name
            title = request.POST.get("title", '').strip()

            file_type = filetype.guess(uploaded_file.read())  # Detect file type
            uploaded_file.seek(0)  # Reset file pointer after reading

            if file_type and file_type.extension in allowed_types:
                # Save the file temporarily to a location
                temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', file_name)
                os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

                # Save the uploaded file to the temporary path
                with open(temp_file_path, 'wb') as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)

                # Now process the file with pymupdf
                try:
                    markdown_text = pymupdf4llm.to_markdown(temp_file_path)

                    # Optionally, save the file in the database if needed
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.original_filename = file_name
                    instance.filesize = uploaded_file.size
                    instance.content = markdown_text
                    instance.title = title
                    instance.save()

                    # Show success message and render
                    messages.success(request, "File uploaded successfully!")
                    return render(request, 'documents/document-list.html', {'markdown_text': markdown_text})
                except Exception as e:
                    messages.error(request, f"Error processing the file: {e}")
                    return render(request, 'documents/document-list.html', {"form": form})

            else:
                messages.error(request, "Invalid filetype. Only PDF files are allowed.")
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
        title = request.POST.get("title", '').strip()
        print(request.POST)


        # Check if the text is empty
        if not text:
            messages.error(request, "Text field cannot be empty.")
            return redirect('document-list')

        if not title:
            messages.error(request, "Title field cannot be empty.")
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
        job_listing = UploadedJobListing(user=user, content=text, filepath=filepath, title=title)
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
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class UploadedResumeDetail(APIView):
#    permission_classes = [IsAuthenticated]

#    def get(self, request, pk):
#        # Use get_object_or_404 to return 404 when the object is not found
#        file = get_object_or_404(UploadedResume, pk=pk, user=request.user)
#        serializer = UploadedResumeSerializer(file)
#        return Response(serializer.data)

#    def put(self, request, pk):
#        # Use get_object_or_404 to return 404 when the object is not found
#        file = get_object_or_404(UploadedResume, pk=pk, user=request.user)
#        serializer = UploadedResumeSerializer(file, data=request.data, partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    def delete(self, request, pk):
#        # Use get_object_or_404 to return 404 when the object is not found
#        file = get_object_or_404(UploadedResume, pk=pk, user=request.user)
#        file.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)


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


#class JobListingDetail(APIView):
#    permission_classes = [IsAuthenticated]

#    def get(self, request, pk):
        # Use get_object_or_404 to return 404 when the object is not found
#        text = get_object_or_404(UploadedJobListing, pk=pk, user=request.user)
#        serializer = UploadedJobListingSerializer(text)
#        return Response(serializer.data)

#    def put(self, request, pk):
#        # Use get_object_or_404 to return 404 when the object is not found
#        text = get_object_or_404(UploadedJobListing, pk=pk, user=request.user)
#        serializer = UploadedJobListingSerializer(text, data=request.data, partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    def delete(self, request, pk):
        # Use get_object_or_404 to return 404 when the object is not found
#        text = get_object_or_404(UploadedJobListing, pk=pk, user=request.user)
#        text.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentList(View):
    def get(self, request):
        return render(request, 'documents/document-list.html')