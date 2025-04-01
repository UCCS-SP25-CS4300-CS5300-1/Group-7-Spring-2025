import os
from django.conf import settings

def handle_uploaded_file(f):
    #Ensure the directory exists.
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, f.name)

    #Writes the file in binary mode.
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path
handle_uploaded_file()
