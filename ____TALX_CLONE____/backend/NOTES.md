# make the remigration
```sh
# app_name app which contains models
./manage.py migrate app_name  zero
./manage.py makemigrations
./manage.py migrate

# also we can make the migrations like
./manage.py makemigrations app_name
./manage.py migrate
# instead of
./manage.py makemigrations
./manage.py migrate

```

# in  my  Dango social media app  project ____TALX____ im traing to register  a user for test purposes  but there are a n issues
- running server output :
```sh
mohamed@DESKTOP-S296B4S /mnt/c/Users/Active/Desktop/Coding/Short_Specializations/Portfolio_project/____TALX_CLONE____/backend
 % ./manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 11, 2024 - 10:53:37
Django version 4.2.10, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

Internal Server Error: /api/register/
Traceback (most recent call last):
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/core/handlers/base.py", line 220, in _get_response
    response = response.render()
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/template/response.py", line 114, in render
    self.content = self.rendered_content
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/response.py", line 74, in rendered_content
    ret = renderer.render(self.data, accepted_media_type, context)
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/renderers.py", line 727, in render
    context = self.get_context(data, accepted_media_type, renderer_context)
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/renderers.py", line 658, in get_context
    raw_data_post_form = self.get_raw_data_form(data, view, 'POST', request)
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/renderers.py", line 578, in get_raw_data_form
    media_types = [parser.media_type for parser in view.parser_classes]
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/renderers.py", line 578, in <listcomp>
    media_types = [parser.media_type for parser in view.parser_classes]
AttributeError: type object 'AllowAny' has no attribute 'media_type'
[11/Jul/2024 10:53:45] "GET /api/register/ HTTP/1.1" 500 88080


```
- my code
```py
 % cat api/*.py
#backend/api/__init__.py#backend/api/admin.py
from django.contrib import admin

# Register your models here.
#backend/api/apps.py
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
#backend/api/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

time_format = "%Y-%m-%dT%H:%M:%S.%f"

class Base(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict['ID'] = str(new_dict['ID'])
        new_dict['created_date'] = new_dict['created_date'].strftime(time_format)
        new_dict['updated_date'] = new_dict['updated_date'].strftime(time_format)
        new_dict.pop('_state', None)
        return new_dict

    class Meta:
        abstract = True

class Users(Base, User):

    def __str__(self):
        return self.username



class Profile(Base):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    profileimg = models.ImageField(
        upload_to="profile_images",
        default="profile_images/blank-profile-picture.png",
    )

    def __str__(self):
        return self.user.username

class Post(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_image/", null=True, blank=True)
    type = models.CharField(
        max_length=4,  choices=[("meme", "Meme"), ("info", "Info")]
    )
class LikePost(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username} like {self.post}"
class Comment(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    content = models.CharField(max_length=500)

class Following(Base):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        Users, on_delete= models.CASCADE, related_name="followers"
    )
    class Meta:
        unique_together = ("user", "followed_user")

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"#backend/api/serializers.py
from rest_framework import serializers
from .models import (
   Base, Users, Profile, Post, LikePost, Comment, Following
    )



class BaseSerializer(serializers.ModelSerializer):
    ID = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = Base
        fields = ("ID", "created_date", "updated_date")
        read_only_fields = ("ID", "created_date", "updated_date")

class UsersSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Users
        fields = ("ID", "id", "email", "username", "first_name", "last_name")
        read_only_fields = ("ID", "id")


class ProfileSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = UsersSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = UsersSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class FollowingSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    followed_user = UsersSerializer(read_only=True)

    class Meta:
        model = Following
        fields = "__all__"
#backend/api/test.py
from django.test import TestCase

# Create your tests here.
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegister.as_view(), name="register"),
    path('register/', views.UserRegister.as_view()),
    path('test', views.test, name='test'),
]
#backend/api/validations.py

from django.core.exceptions import ValidationError
from .models import Users


def custom_validation(data):
    email = data["email"].strip()
    username = data["username"].strip()
    password = data["password"].strip()
    ##
    if not email or Users.objects.filter(email=email).exists():
        raise ValidationError("choose another email")
    ##
    if not password or len(password) < 8:
        raise ValidationError("choose another password, min 8 characters")
    ##
    if not username:
        raise ValidationError("choose another username")
    return data


def validate_email(data):
    email = data["email"].strip()
    if not email:
        raise ValidationError("an email is needed")
    return True


def validate_username(data):
    username = data["username"].strip()
    if not username:
        raise ValidationError("choose another username")
    return True


def validate_password(data):
    password = data["password"].strip()
    if not password:
        raise ValidationError("a password is needed")
    return True
#backend/api/views.py
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, status, generics
from .validations import custom_validation, validate_email, validate_password


from .models import (
    Users, Post, Profile, LikePost, Comment, Following
)
from .serializers import (
    UsersSerializer,
    PostSerializer,
    ProfileSerializer,
    LikePostSerializer,
    CommentSerializer,
    FollowingSerializer,
)
from rest_framework.decorators import api_view

@api_view(['GET'])
def test(request):
    data = {'message': 'Test successful'}
    return Response(data)
class UserRegister(APIView):
    parser_classes = (permissions.AllowAny, )
    def post(self, request):
        clean_data = custom_validation(request.data)
        print(f"\n\n::   clean_data ${clean_data}   >>  \n\n")
        serializer = UsersSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
mohamed@DESKTOP-S296B4S /mnt/c/Users/Active/Desktop/Coding/Short_Specializations/Portfolio_project/____TALX_CLONE____/backend
```