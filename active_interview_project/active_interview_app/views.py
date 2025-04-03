from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *  # Keep models from main
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, CreateUserForm  # Ensure both forms are imported
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from rest_framework.permissions import IsAuthenticated
import filetype
import pymupdf4llm


# Create your views here.

allowed_types = ['pdf']

def index(request):
    return render(request, "index.html")


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            type_of_file = filetype.guess(uploaded_file.read())

            if type_of_file and type_of_file.extension in allowed_types:
                form.save()
                markdown_text = pymupdf4llm.to_markdown(upload_file)
                messages.success(request, "File uploaded successfully!")
                return HttpResponseRedirect("/")
            else:
                messages.error(request, "Invalid filetype. Please upload a .pdf.")
    else:
        form = UploadFileForm()
    return render(request, "index.html", {"form": form})

#Entire CRUD stack/views for the file. User should be able to modify/read/access files. Tests. 

'''
    import filetype
    
    def check_file_type(file_path, allowed_types):
        kind = filetype.guess(file_path)
        if kind is None:
            return False
    
        if kind.extension in allowed_types:
             return True
        return False
    
    allowed_types = ['txt', 'pdf', 'jpg', 'png']
    file_path = 'example.pdf'
    if check_file_type(file_path, allowed_types):
        print("File type is allowed.")
    else:
        print("File type is not allowed.")
        '''


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
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadedFileDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            file = UploadedFile.objects.get(pk=pk, user=request.user)
        except UploadedFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UploadedFileSerializer(file)
        return Response(serializer.data)

    def put(self, request, pk):
        #Update file metadata.
        try:
            file = UploadedFile.objects.get(pk=pk, user=request.user)
        except UploadedFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UploadedFileSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            file = UploadedFile.objects.get(pk=pk, user=request.user)
        except UploadedFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

