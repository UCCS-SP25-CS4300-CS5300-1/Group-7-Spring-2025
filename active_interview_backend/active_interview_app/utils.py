import os
from django.conf import settings
import logging


def handle_uploaded_file(f):
    #Ensure the directory exists.
    try:
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, f.name)

        #Writes the file in binary mode.
        with open(file_path, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return file_path
    except PermissionError as e:
        logger.error(f"Permission error while saving file: {e}")
        raise ValueError(
            "There was an error saving the file. Please try again later.")

    except Exception as e:
        logger.error(f"Unexpected error while saving file: {e}")
        raise ValueError(
            "An unexpected error occurred. Please try again later.")

handle_uploaded_file()
