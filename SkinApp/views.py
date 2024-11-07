from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import cv2
from keras.models import Sequential, load_model, Model

# Use the Agg backend for Matplotlib
import matplotlib
matplotlib.use('Agg')

global uname
vgg_model = load_model("model/vgg_weights.keras")

#use this function to predict fish species uisng extension model
def predict(image_path):
    global vgg_model
    labels = ['Benign', 'Malignant']
    image = cv2.imread(image_path)#read test image
    img = cv2.resize(image, (128,128))#resize image
    im2arr = np.array(img)
    im2arr = im2arr.reshape(1,128,128,3)#convert image as 4 dimension
    img = np.asarray(im2arr)
    img = img.astype('float32')#convert image features as float
    img = img/255 #normalized image
    pred = vgg_model.predict(img)#now predict type of skin lesion
    predict = np.argmax(pred)
    score = np.amax(pred)
    img = cv2.imread(image_path)
    img = cv2.resize(img, (600,400))#display image with predicted output
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.putText(img, 'Predicted : '+labels[predict]+" Score : "+str(score), (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (255, 0, 0), 2)
    return img

# def UploadAction(request):
#     if request.method == 'POST':
#         global uname
#         image = request.FILES['t1']
#         imagename = request.FILES['t1'].name
#         fs = FileSystemStorage()
#         if os.path.exists('SkinApp/static/skin/'+imagename):
#             os.remove('SkinApp/static/skin/'+imagename)
#         filename = fs.save('SkinApp/static/skin/'+imagename, image)
#         img = predict('SkinApp/static/skin/'+imagename)
#         plt.imshow(img)
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png', bbox_inches='tight')
#         plt.close()
#         img_b64 = base64.b64encode(buf.getvalue()).decode()
#         context= {'data': 'Predicted Output', 'img': img_b64}
#         return render(request, 'UserScreen.html', context)

def UploadAction(request):
    if request.method == 'POST':
        global uname
        image = request.FILES['t1']
        imagename = request.FILES['t1'].name
        fs = FileSystemStorage()
        if os.path.exists('SkinApp/static/skin/'+imagename):
            os.remove('SkinApp/static/skin/'+imagename)
        filename = fs.save('SkinApp/static/skin/'+imagename, image)
        img = predict('SkinApp/static/skin/'+imagename)
        
        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.imshow(img)
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        
        # Encode the image in base64
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        
        # Pass the base64 image to the context
        context = {'data': 'Predicted Output:', 'img': img_b64}
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
            context= {'data':""}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'index.html', context)        

