from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegister.as_view(), name="register"),
    path('register/', views.UserRegister.as_view()),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
    path('post/', views.AddPost.as_view(), name='post'),
    path('comment/', views.AddComment.as_view(), name='comment'),
    path('like/', views.Like.as_view(), name='like'),
    path('get_all/', views.GetAllByToken.as_view(), name='get_all'),
    path('post/comments', views.PostComments.as_view(), name='post_comments'),

    path('test', views.test, name='test'),
    path('test2', views.test2, name='test2'),
    path('test3', views.test3, name='test3'),
]
