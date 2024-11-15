from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index"),      
               path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
	       path("Upload.html", views.Upload, name="Upload"),	      
               path("UploadAction", views.UploadAction, name="UploadAction"),
               path('delete_image', views.delete_image, name='delete_image'),
               	       
]
