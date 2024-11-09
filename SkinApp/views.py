# from django.shortcuts import render
# from django.template import RequestContext
# from django.contrib import messages
# from django.http import HttpResponse
# import os
# from django.core.files.storage import FileSystemStorage
# import matplotlib.pyplot as plt
# import io
# import base64
# import numpy as np
# import cv2
# from django.shortcuts import render
# from django.template import RequestContext
# from django.contrib import messages
# from django.http import HttpResponse

# # from keras.models import load_model

# # Use the Agg backend for Matplotlib
# # import matplotlib
# # matplotlib.use('Agg')

# # global uname
# # vgg_model = load_model("model/vgg_weights.keras")

# #use this function to predict fish species uisng extension model
# # def predict(image_path):
# #     global vgg_model
# #     labels = ['Benign', 'Malignant']
# #     image = cv2.imread(image_path)#read test image
# #     img = cv2.resize(image, (128,128))#resize image
# #     im2arr = np.array(img)
# #     im2arr = im2arr.reshape(1,128,128,3)#convert image as 4 dimension
# #     img = np.asarray(im2arr)
# #     img = img.astype('float32')#convert image features as float
# #     img = img/255 #normalized image
# #     pred = vgg_model.predict(img)#now predict type of skin lesion
# #     predict = np.argmax(pred)
# #     score = np.amax(pred)
# #     img = cv2.imread(image_path)
# #     img = cv2.resize(img, (600,400))#display image with predicted output
# #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #     cv2.putText(img, 'Predicted : '+labels[predict]+" Score : "+str(score), (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (255, 0, 0), 2)
# #     return img

# # def UploadAction(request):
# #     if request.method == 'POST':
# #         global uname
# #         image = request.FILES['t1']
# #         imagename = request.FILES['t1'].name
# #         fs = FileSystemStorage()
# #         # if os.path.exists('SkinApp/static/skin/'+imagename):
# #         #     os.remove('SkinApp/static/skin/'+imagename)
# #         filename = fs.save('SkinApp/static/skin/'+imagename, image)
# #         img = predict('SkinApp/static/skin/'+imagename)
        
# #         # Save the plot to a buffer
# #         buf = io.BytesIO()
# #         plt.imshow(img)
# #         plt.savefig(buf, format='png', bbox_inches='tight')
# #         plt.close()
        
# #         # Encode the image in base64
# #         img_b64 = base64.b64encode(buf.getvalue()).decode()
        
# #         # Pass the base64 image to the context
# #         context = {'data': 'Predicted Output:', 'img': img_b64}
# #         os.remove('SkinApp/static/skin/'+imagename) #added this line
# #         return render(request, 'UserScreen.html', context)


# def UploadAction(request):
#     if request.method == 'POST':
#         image = request.FILES['t1']
#         imagename = request.FILES['t1'].name
#         # Save the image path for later use in the template (optional)
#         image_path = os.path.join('SkinApp/static/skin/', imagename)
#         fs = FileSystemStorage()
#         filename = fs.save(image_path, image)
        
#         # Context for the template (no prediction data included)
#         context = {'data': 'Predicted Output:', 'image_path': image_path}  # Pass image path to template
#         return render(request, 'UserScreen.html', context)

# def UserLogin(request):
#     if request.method == 'GET':
#        return render(request, 'UserLogin.html', {})    

# def index(request):
#     if request.method == 'GET':
#        return render(request, 'index.html', {})

# def Upload(request):
#     if request.method == 'GET':
#         return render(request, 'Upload.html', {})    

# def UserLoginAction(request):
#     if request.method == 'POST':
#         username = request.POST.get('t1', False)
#         password = request.POST.get('t2', False)
#         if username == 'admin' and password == 'admin':
#             context= {'data':""}
#             return render(request, 'UserScreen.html', context)
#         else:
#             context= {'data':'login failed'}
#             return render(request, 'index.html', context)        

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.templatetags.static import static
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


def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Upload(request):
    if request.method == 'GET':
        return render(request, 'Upload.html', {})    

def UserLoginAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            return render(request, 'UserScreen.html', {})
        else:
            context = {'data': 'login failed'}
            return render(request, 'index.html', context)
