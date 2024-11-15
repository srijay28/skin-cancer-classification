from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.templatetags.static import static
from django.conf import settings
from django.http import JsonResponse
from urllib.parse import unquote
import os
import base64
import io


def UploadAction(request):
    if request.method == 'POST':
        image = request.FILES['t1']
        imagename = request.FILES['t1'].name
        fs = FileSystemStorage()

        # Save the uploaded image to the static directory for client access
        filename = fs.save(f'SkinApp/static/skin/{imagename}', image)

        # Construct the static URL correctly
        image_url = static(f'skin/{imagename}')
        
        # Pass the image URL to the client for TensorFlow.js processing
        context = {'image_url': image_url}
        return render(request, 'UserScreen.html', context)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def delete_image(request):
    print("delete_image called")
    image_url = request.GET.get("image_url")
    if image_url:
        # Decode the URL and determine the file path
        relative_path = unquote(image_url.replace(settings.STATIC_URL, ''))
        # Modify the file path for deletion
        file_path = os.path.join(settings.BASE_DIR, 'SkinApp/static', relative_path)



        # Print or log file path details
        print(f"Attempting to delete: {file_path}")

        # Check if the file exists and delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Image deleted successfully.")
            return JsonResponse({"status": "success", "message": "Image deleted"})
        else:
            print("File does not exist.")
            return JsonResponse({"status": "error", "message": "File not found"})

    print("No image URL provided.")
    return JsonResponse({"status": "error", "message": "No image URL provided"})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})    

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def Upload(request):
    if request.method == 'GET':
        return render(request, 'Upload.html', {})    

def UserLoginAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        return render(request, 'UserScreen.html', {})
