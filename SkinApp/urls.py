from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index"),
               path("UserLogin.html", views.UserLogin, name="UserLogin"),	      
               path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
	       path("Upload.html", views.Upload, name="Upload"),	      
               path("UploadAction", views.UploadAction, name="UploadAction"),
               	       
]
