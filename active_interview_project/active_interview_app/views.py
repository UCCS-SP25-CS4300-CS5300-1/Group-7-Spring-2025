# views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm

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
