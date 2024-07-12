from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegister.as_view(), name="register"),
    path('register/', views.UserRegister.as_view()),
     path('login/', views.UserLogin.as_view(), name='user_login'),

    path('test', views.test, name='test'),
    path('test2', views.test2, name='test2'),
]
