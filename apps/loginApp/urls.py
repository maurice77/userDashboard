
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gotoIndex,name='home'),
    path('signin', views.gotoLogin, name='signin'),
    path('register',views.gotoRegister, name='register'),
    path('success',views.showSuccess),
    path('login/signout',views.signOut, name='signout'),
    path('register/checkEmail',views.checkEmail),
]