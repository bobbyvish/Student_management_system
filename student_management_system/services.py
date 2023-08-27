import os 
import uuid
from pathlib import Path
from django.core.files.uploadedfile import UploadedFile
from . import settings
import logging

logger = logging.getLogger(__name__)

# INFO file_types
# Text files: text/plain
# HTML files: text/html
# CSS files: text/css
# JavaScript files: application/javascript
# JSON files: application/json
# XML files: application/xml
# PDF files: application/pdf
# Word documents: application/msword
# Excel spreadsheets: application/vnd.ms-excel
# PowerPoint presentations: application/vnd.ms-powerpoint
# Images:
# JPEG files: image/jpeg
# PNG files: image/png
# GIF files: image/gif
# BMP files: image/bmp
# Audio files:
# MP3 files: audio/mpeg
# WAV files: audio/wav
# Video files:
# MP4 files: video/mp4
# AVI files: video/x-msvideo


# Example code how to use uploadservice in your view

"""
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            allowed_types = ['image/png', 'image/jpeg']
            allowed_extensions = ['.png', '.jpg', '.jpeg']
            upload_service = UploadService(allowed_types=allowed_types, allowed_extensions=allowed_extensions)
            try:
                url = upload_service.upload(file, settings.MEDIA_ROOT)
            except ValueError as e:
                # Handle validation error
                return HttpResponse(str(e), status=400)
            except Exception as e:
                # Handle other errors
                return HttpResponse(str(e), status=500)
            # File uploaded successfully, render success message
            return render(request, 'success.html', {'url': url})
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

"""







class UploadServices:
    def __init__(self, allowed_types = None, allowed_extensions= None, max_size= None):
        self.allowed_types = allowed_types
        self.allowed_extensions = allowed_extensions
        self.max_size = max_size

    def _validate_file_type(self,file):
        # check if the file's content type is allowed
        if self.allowed_types and file.content_type not in self.allowed_types:
            raise ValueError(f"Invalid file type. Allowed file types are:{', '.join(self.allowed_types)}")

    def _validate_file_extension(self,file):
        # Check if the file's extension is allowed
        if self.allowed_extensions and not file.name.endswith(tuple(self.allowed_extensions)):
            raise ValueError(f"Invalid file extension. Allowed file extensions are:{', '.join(self.allowed_extensions)}")

    # def _validate_file_size(self, file):
    #     # Check if the file's size is within the allowed limit
    #     if self.max_size and file.size > self.max_size:
    #         raise ValueError(f"File size is too large. Maximum allowed size is {self.max_size} bytes.")


    def upload(self, file,file_name=None, destination=None):
        # Check if the file is an instance of UploadedFile
        if not isinstance(file, UploadedFile):
            raise ValueError(f"Expected file type UploadedFile. Given {type(file)}")

        # Validate the file's type and extension
        self._validate_file_type(file)
        self._validate_file_extension(file)
        # self._validate_file_size(file)

        # Generate a unique file name using uuid
        random_str = str(uuid.uuid4())
        ext = os.path.splitext(file.name)[1].lower()
        filename = f"{file_name}_{random_str}{ext}" if file_name else f"{random_str}{ext}"
        
        # Create the file path
        if destination is not None:
            filename_to_store = os.path.join(destination, filename)
            folder = os.path.join(settings.MEDIA_ROOT, destination)
            Path(folder).mkdir(parents=True, exist_ok=True)
            filepath = os.path.join(folder, filename)
        else:
            filename_to_store = filename
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
        
        # Save the file to disk
        try:
            with open(filepath, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        except Exception as e:
            # define logger for error
            logger.error(e)
            return False

        # Return the file path, including the destination folder if specified
        return filename_to_store

        