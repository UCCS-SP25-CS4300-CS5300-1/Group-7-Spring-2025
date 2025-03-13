import os

def handle_uploaded_file(f):
    #Ensure the directory exists.
    upload_dir = "uploads/"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f.name)

    #Writes the contents of the file in binary mode to our specified path.
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path