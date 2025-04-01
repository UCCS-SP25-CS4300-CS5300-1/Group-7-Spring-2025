# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *  # Keep models from main
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, CreateUserForm  # Ensure both forms are imported

# Create your views here.
def index(request):
    return render(request, "index.html")


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Save file to the database
            return HttpResponseRedirect("/")
    else:
        form = UploadFileForm()
    return render(request, "index.html", {"form": form})


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
