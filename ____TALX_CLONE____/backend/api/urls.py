from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegister.as_view(), name="register"),
    path('register/', views.UserRegister.as_view()),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),

    path('test', views.test, name='test'),
    path('test2', views.test2, name='test2'),
    path('test3', views.test3, name='test3'),
]
