from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *  # Keep models from main
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, CreateUserForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedFile
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.conf import settings
import filetype
import pymupdf4llm
import os


# Create your views here.

allowed_types = ['pdf']

def index(request):
    return render(request, "index.html")


@login_required
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            file_name = uploaded_file.name


            file_type = filetype.guess(uploaded_file.read())
            uploaded_file.seek(0)

            if file_type and file_type.extension in allowed_types:

                instance = form.save(commit=False)
                instance.user = request.user
                instance.original_filename = file_name
                instance.filesize = uploaded_file.size
                instance.save()

                uploaded_file_url = os.path.join(settings.MEDIA_URL, file_name)
                markdown_text = pymupdf4llm.to_markdown(uploaded_file)
                messages.success(request, "File uploaded successfully!")
                return render(request, 'index.html', {'uploaded_file_url': uploaded_file_url})
            else:
                messages.error(request, "Invalid filetype. Please upload a .pdf.")
    else:
        form = UploadFileForm()
    return render(request, "index.html", {"form": form})

class PastedTextView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.POST.get("text", '').strip()
        if not text:
            messages.error(request, "Text field cannot be empty.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        user = request.user
        timestamp = now().strftime("%d%m%Y_%H%M%S")
        filename = f"{user.username}_{timestamp}.txt"

        user_dir = os.path.join(settings.MEDIA_ROOT, 'pasted_texts', str(user.id))
        os.makedirs(user_dir, exist_ok=True)
        filepath = os.path.join(user_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        messages.success(request, "Text uploaded successfully!")
        return redirect(request.META.get('HTTP_REFERER', '/'))




@login_required
def loggedin(request):
    return render(request, 'loggedinindex.html')

def register(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        group = Group.objects.get(name='manager_role')
        user.groups.add(group)
        # user = User.objects.create(user=user)  # Keep this comment from main
        user.save()
        messages.success(request, 'Account was created for ' + username)
        return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('logout')
    return render(request, 'logout.html')


class UploadedFileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        files = UploadedFile.objects.filter(user=request.user)
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UploadedFileSerializer(data=request.data)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UploadedFileDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        file = UploadedFile.objects.get(pk=pk, user=request.user)


        serializer = UploadedFileSerializer(file)
        return Response(serializer.data)

    def put(self, request, pk):
        file = UploadedFile.objects.get(pk=pk, user=request.user)


        serializer = UploadedFileSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        file = UploadedFile.objects.get(pk=pk, user=request.user)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class PastedTextList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ List all pasted text entries for the authenticated user """
        texts = PastedText.objects.filter(user=request.user)
        serializer = PastedTextSerializer(texts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Create a new pasted text entry """
        serializer = PastedTextSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PastedTextDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """ Retrieve a specific pasted text entry by id """
        text = PastedText.objects.get(pk=pk, user=request.user)


        serializer = PastedTextSerializer(text)
        return Response(serializer.data)

    def put(self, request, pk):
        """ Update a specific pasted text entry by id """
        text = PastedText.objects.get(pk=pk, user=request.user)


        serializer = PastedTextSerializer(text, data=request.data, partial=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        """ Delete a specific pasted text entry by id """
        text = PastedText.objects.get(pk=pk, user=request.user)

        text.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)