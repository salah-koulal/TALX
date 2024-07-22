
#backend/api/__init__.py
from rest_framework import status
from .validations import Validator

validator = Validator()
S200 = status.HTTP_200_OK
S201 = status.HTTP_201_CREATED
S304 = status.HTTP_304_NOT_MODIFIED
S400 = status.HTTP_400_BAD_REQUEST
S401 = status.HTTP_401_UNAUTHORIZED
S405 = status.HTTP_405_METHOD_NOT_ALLOWED
S404 = status.HTTP_404_NOT_FOUND
from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)

# admin.site.register(Users)#backend/api/apps.py
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
#backend/api/authentication.py
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status

from .validations import *
from .models import *
from .serializers import *

class Authentication:
    def __init__(self) -> None:
        self.cookies_session = []
        self.logged_users = []
        self.tokens_list = []

    def reload(self):
        self.logged_users = [cookie["username"] for cookie in self.cookies_session]
        self.tokens_list = [cookie["token"] for cookie in self.cookies_session]

    def new_token(self, username: str, exp: int) -> str:
        secret_key = "HORIZONS-SECRET-KEY"

        payload = {
            "username": username,
            "exp": datetime.utcnow() + timedelta(days=exp)
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')


    def is_logged(self, username:str=None, token:str=None) -> bool:
        self.reload()
        if username and username in self.logged_users:
            return True
        if token and token in self.tokens_list:
            return True
        return False

    def get_by(self, token: str = None, username: str = None) -> str:
        if token:
            for cookie in self.cookies_session:
                if cookie["token"] == token:
                    return  cookie["username"]
        if username:
            for cookie in self.cookies_session:
                if cookie["username"] == username:
                    return cookie["token"]
        return None


    def all(self, to_return="logged_users"):
        self.reload()
        if to_return == "logged_users":
            return self.logged_users
        elif to_return == "tokens":
            return self.tokens_list
        else:
            return self.cookies_session

    def register_user(self, request):

        # Validate the incoming data
        data = request.data["user"] or request.data
        clean_data = custom_validation(data)

        if "password" in clean_data:
            clean_data["password"] = make_password(clean_data["password"])
        # Create the user instance
        user = Users(**clean_data)
        user.save()
        if user:
            # Create and save the profile for the new user
            profile = Profile(user=user)
            profile.save()
            # Include profile data in the response
            user_data =  UsersSerializer(user).data
            user_data['profile'] = ProfileSerializer(profile).data

            # Return the user data along with profile data
            return Response(user_data, status=status.HTTP_201_CREATED)
        # Return bad request status if the serializer is not valid
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def login_username(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = Users.objects.filter(username=username).first()
        if user is None:
            return Response({'detail': f'{username} does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
        if not authenticate(username=username, password=password):
            return Response({'detail': 'Password incorrect'}, status=status.HTTP_401_UNAUTHORIZED)

        token = self.new_token(username, 1)
        user_found = False
        # check if the user is already logged in
        for cookie in self.cookies_session:
            if cookie.get("username") == username:
                cookie["token"] = token
                user_found = True
                break

        if not user_found:
            self.cookies_session.append({"token": token, "username": username})

        profiles = Profile.objects.filter(user=user).first()
        serial_data = ProfileSerializer(profiles).data
        return Response((serial_data, token), status=status.HTTP_200_OK)

    def logout_username(self, request):
        username = request.data.get("username")
        self.reload()
        if username:
            if username in self.logged_users:
                for cookie in self.cookies_session:
                    if cookie["username"] == username:
                        self.cookies_session.remove(cookie)
                        return Response({"detail": f"{username} logged out"}, status=status.HTTP_200_OK)
                # This block is theoretically unreachable due to previous check
                return Response({"detail": f"No active session found for {username}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": f"{username} is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)
from .models import *
from .serializers import *
from validations import *
def get_object(request):
    data = request.data or None
    cls_name = data.get("class") or None
    obj_id = data.get("ID") or None
    query_obj = classes[cls_name].objects.filter(ID=obj_id).first()
    serial_obj = query_obj.to_dict()  if query_obj else None
    if serial_obj:
        return (True, serial_obj, data.get("new") or None, query_obj)
    issues  = ""
    issues += "request data" if data is None else ""
    issues += ", object class name " if cls_name is None else ""
    issues += f" ,id object {obj_id} issue" if query_obj is None else ""
    issues += f" ,serialize issue" if serial_obj is None else ""
    return (False, issues)

def update_user(user_obj, news_dict):
    pass
from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django.contrib.auth.hashers import make_password
from .__init__ import validator

time_format = "%Y-%m-%dT%H:%M:%S.%f"

class Base(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # def update(self, new=None):
        # self.updated_date = datetime.now()
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict['ID'] = str(new_dict['ID'])
        if "created_date" in new_dict:
            new_dict['created_date'] = new_dict['created_date'].strftime(time_format)
        if "updated_date" in new_dict:
            new_dict['updated_date'] = new_dict['updated_date'].strftime(time_format)
        new_dict.pop('_state', None)
        if 'date_joined' in new_dict:
            new_dict['date_joined'] = new_dict['date_joined'].strftime(time_format)
        if 'password' in new_dict:
            new_dict.pop("password")
        if 'user_id' in new_dict:
            new_dict['user_id'] = str(new_dict['user_id'])
        return new_dict

    class Meta:
        abstract = True

class Users(Base, User):
    def update_user(self, data_obj=None, **kwargs):
        if not data_obj and kwargs:
            return (False, "no data to update")
        if data_obj is None:
            result = validator.all(data_object=kwargs, all_required=False)
        result = validator.all(data_object=data_obj, all_required=False)
        if not result[0]:
            return result
        clean_data = result[1]
        similar_val_ky = []
        for key in clean_data:
            if key == "password":
                clean_data["password"] =  make_password(clean_data["password"])
            if self.key  == clean_data[key]:
                similar_val_ky.append(key)
                continue
            self.key = clean_data[key]
        if len(similar_val_ky) == len(clean_data.keys()):
            return (False, "".join(similar_val_ky) + "are tje same")
        self.updated_date = datetime.now()
        self.save()
        return (True, self.to_dict())
    def __str__(self):
        return self.username

class Profile(Base):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
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
        max_length=4, choices=[("meme", "Meme"), ("info", "Info")]
    )
    likes = models.ManyToManyField(
        Users, related_name="liked_posts", blank=True
    )
    dislikes = models.ManyToManyField(
        Users, related_name="disliked_posts", blank=True
    )

    def __str__(self):
        return f"{self.author.username}'s post"


class Comment(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    likes = models.ManyToManyField(
        Users, related_name="liked_comments", blank=True
    )
    dislikes = models.ManyToManyField(
        Users, related_name="disliked_comments", blank=True
    )

    def __str__(self):
        return f"{self.author.username}'s comment on {self.post}"

class Following(Base):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="followers"
    )

    class Meta:
        unique_together = ("user", "followed_user")

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"

class Report(Base):
    REPORT_CHOICES = [
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('user', 'User')
    ]
    reported_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="reports_made")
    report_type = models.CharField(max_length=10, choices=REPORT_CHOICES)
    reported_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="reports")
    reported_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name="reports")
    reported_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name="reports_against")
    reason = models.TextField()

    def __str__(self):
        return f"Report by {self.reported_by.username} on {self.report_type}"
classes = {
    "Comment":Comment, "Users":Users, "Post":Post,
    "Following":Following, "Report":Report
}
#backend/api/serializers.py
from rest_framework import serializers
from .models import *



class BaseSerializer(serializers.ModelSerializer):
    ID = serializers.UUIDField(source='ID', read_only=True)  # Ensure 'ID' comes from the 'ID' field

    class Meta:
        model = Base
        fields = ("ID", "created_date", "updated_date")
        read_only_fields = ("ID", "created_date", "updated_date")

class UsersSerializer(BaseSerializer):
    # id = serializers.IntegerField(source='pk', read_only=True)
    ID = serializers.CharField(source='pk', read_only=True)  # Map 'ID' to 'pk' to have same value as 'id'

    class Meta(BaseSerializer.Meta):
        model = Users
        fields = ("ID", "id", "email", "username", "first_name", "last_name")
        read_only_fields = ("id", )


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
'''

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = "__all__"

'''
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
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


'''
class BaseSerializer(serializers.ModelSerializer):
    ID = serializers.UUIDField(read_only=True)  # Ensure 'ID' comes from the 'ID' field

    class Meta:
        model = Base
        fields = ("ID", "created_date", "updated_date")
        read_only_fields = ("ID", "created_date", "updated_date")

class UsersSerializer(BaseSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)  # Explicitly map 'id' to primary key

    class Meta(BaseSerializer.Meta):
        model = Users
        fields = ("ID", "id", "email", "username", "first_name", "last_name")
'''
"""
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model =Users
        fields = "__all__"

    def create(self, clean_data):
        user_obj =Users.objects.create (
            email=clean_data["email"],
            password=clean_data["password"],
            username=clean_data["username"],
            first_name=clean_data["first_name"],
            last_name=clean_data["last_name"],
            user_pt=Base
        )
        user_obj.save()
        x = Profile.objects.create(user=user_obj)
        x.save()

        return user_obj
"""
cls_serializers = {
    "Comment":CommentSerializer, "Users":UsersSerializer, "Post":PostSerializer,
    "Following":FollowingSerializer, "Report":Report
}
#backend/api/test.py
from django.test import TestCase

# Create your tests here.
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
    path('get/object/by/id', views.GetObjectById.as_view(), name="get_byId" ),
    path('update/object/by/id', views.UpdateByID.as_view(), name="update_byId" ),

]
#backend/api/validations.py

from django.core.exceptions import ValidationError
from .models import Users

class Validator:
    concern_keys = ["email", "password", "username", "first_name", "last_name"]

    @staticmethod
    def validate_email(email):
        # Replace this with actual email validation logic
        if "@" in email:
            return True, email
        return False, "Invalid email"

    @staticmethod
    def validate_password(password):
        # Replace this with actual password validation logic
        if len(password) >= 6:
            return True, password
        return False, "Invalid password"

    @staticmethod
    def validate_username(username):
        # Replace this with actual username validation logic
        if username.isalnum():
            return True, username
        return False, "Invalid username"

    @staticmethod
    def validate_first_name(first_name):
        # Replace this with actual first name validation logic
        if first_name.isalpha():
            return True, first_name
        return False, "Invalid first name"

    @staticmethod
    def validate_last_name(last_name):
        # Replace this with actual last name validation logic
        if last_name.isalpha():
            return True, last_name
        return False, "Invalid last name"

    def all(self, data_object, all_required=True):
        """
        Validate all the keys in the data_object.

        :param data_object: A dictionary containing the keys and values to validate.
        :type data_object: dict
        :param all_required: A boolean indicating whether all concern_keys must be present in data_object.
        :type all_required: bool
        :return: A tuple containing a boolean indicating success or failure and either a dictionary of validated data or an error message.
        :rtype: tuple
        """

        missing_keys = [key for key in self.concern_keys if key not in data_object]
        invalid_keys = [key for key in data_object if key not in self.concern_keys]

        if all_required and missing_keys:
            return False, f"{missing_keys} are missing"
        if invalid_keys:
            return False, f"Invalid keys: {invalid_keys}"

        clean_data = {}
        invalid_values = []

        for key, value in data_object.items():
            validate_method = getattr(self, f"validate_{key}", None)
            if validate_method:
                valid, result = validate_method(value)
                if valid:
                    clean_data[key] = result
                else:
                    invalid_values.append(result)

        if invalid_values:
            return False, f"Invalid values: {invalid_values}"

        return True, clean_data

def custom_validation(data):
    email = data["email"].strip()
    username = data["username"].strip()
    password = data["password"].strip()
    ##
    if not email or Users.objects.filter(email=email).exists():
        raise ValidationError("choose another email")
    ##
    if not username or Users.objects.filter(username=username).exists():
        raise ValidationError("choose another username")
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
    return True#backend/api/views.py
import jwt


from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions

from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta


from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
from .authentication import Authentication
from .__init__ import *
from .header import *
######################  GLOBALS ################################

auth = Authentication()
x = {"username":"Kyoko",
     "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ikt5b2tvIiwiZXhwIjoxNzIxMTk0MjcxfQ.wlkL7OrId4K_yO7dBO2HRwjBQwC22rS5gf7H2sAEhrk"

     }
auth.cookies_session.append(x)

###
use_POST = {"detail": f"Please use POST ."}
################# END GLOBALS #########
@api_view(['GET'])
def test(request):
    all_obj = Users.objects.all()
    serial_data2 = UsersSerializer(all_obj, many=True).data
    serial_data = [obj.to_dict() for obj in all_obj]

    return Response((serial_data, serial_data2))
@api_view(['GET'])
def test2(request):
    all_obj = Profile.objects.all()
    serial_data2 = ProfileSerializer(all_obj, many=True).data
    # serial_data = [obj.to_dict() for obj in all_obj]

    return Response( serial_data2)
@api_view(['GET'])
def test3(request):
    auth.reload()
    return Response({
        "logged_users":auth.logged_users, "cookies_session":auth.cookies_session
        } ,status=S200)

class UserRegister(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    def post(self, request):
        return auth.register_user(request)

class getCSRFCookie(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrftoken': csrf_token})

#         return Response({'detail': 'Invalid credentials'}, status=S401)
class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):return Response(use_POST,status=S405)

    def post(self, request):

        return auth.login_username(request)

class UserLogout(APIView):
    def get(self, request):
        return Response({"detail": "Please use POST to logout."},
                        status=S405)

    def post(self, request):
        return auth.logout_username(request)

class AddPost(APIView):
    def get(self, request): return Response(use_POST, status=S405)
    def post(self, request):
        required = {"token", "post"}
        req_post = {"author", "content", "type"}

        if request  and request.data and required.issubset(request.data.keys()):
            post_data = request.data["post"]
            print(f"\n\n\n :: from AddPost >>  {post_data} ")
            token    = request.data.get("token")
            username =  auth.get_by(token)
            if auth.is_logged(token=token):

                if not req_post.issubset(post_data.keys()):
                    return Response([{"Error":f"{req_post} are required"}, req_post,request.data],
                                    status=S400)

                author = Users.objects.filter(username=username).first()
                serialized_user = author.to_dict()

                post_data["author"] = author
                post_obj = Post(**post_data)
                post_obj.save()
                saved_post = post_obj
                serialized_post = PostSerializer(saved_post).data
                saved_post = Post.objects.filter(author=author).first()
                return Response(saved_post.to_dict() ,
                                status=S200)
        return Response(status=S400)
class AddComment(APIView):
    def get(self, request):return Response(use_POST, status=S405)

    def post(self, request):
        if not request or not  request.data :
            return Response(status=S400)
        data = request.data["comment"] or None
        token = request.headers.get('Authorization') or request.data["token"] or None

        if not data or not token:

            return Response({"messing":"asdas"} , status=S400)
        author_name = auth.get_by(token=token)
        if not author_name:
            return Response(status=S401)

        author = Users.objects.filter(username=author_name).first()
        if not author:
            return Response({"Error":f"{author_name} not found"})


        post_id = data["post_id"] or None
        content = data["content"] or None

        if not post_id or not content:
                return Response({"messing":"comment and post_id required "},
                                status=S400)

        post_obj = Post.objects.filter(ID=post_id).first()
        if not post_obj:
            return Response({"Error":f"{post_id} is not a valid id "},
                            status=S304)
        comment ={
            "author":author, "post":post_obj, "content":content
        }
        comment_obj = Comment(**comment)
        comment_obj.save()
        ser_comment = CommentSerializer(comment_obj).data
        return Response(ser_comment, status=S201)




class GetAllByToken(APIView):
    def get(self, request): return Response(use_POST, status=S405)

    def post(self, request):
        token = request.headers.get('Authorization') or request.data["token"] or None
        username = auth.get_by(token=token) or None
        if not username:
            return Response(status=S401)
        data = request.data or None
        if not data:
            return Response({"Error": "Request data missing"},
                            status=S400)
        response_obj = {}
        msg = ""
        user = Users.objects.filter(username=username).first()
        for key in data.keys():
            if key == "token":
                continue
            cls_name = key.lower().strip().capitalize()
            if cls_name  in classes.keys():
                if cls_name in ["Comment", "Post"]:
                    all_objs=classes[cls_name].objects.filter(author=user.ID).all()
                else:
                    all_objs=classes[cls_name].objects.filter(username=username).all()
                # serial_objs=cls_serializers[cls_name](all_objs, many=True).data
                serial_objs = [obj.to_dict() for obj in all_objs]
                response_obj[key] = serial_objs

            else:
                if len(msg) > 0:
                    msg += ", "
                else:
                    msg += "can't find "
                msg += f"{key}"

        if msg == "":
            msg = None


        return Response({"data":response_obj, "issues":msg},
                        status=S200 )

class PostComments(APIView):
    def get(self, request): return Response(use_POST,status=S405)

    def post(self, request):
        token = request.headers.get('Authorization') or request.data["token"] or None
        username = auth.get_by(token=token) or None
        if not username:
            return Response(status=S401)
        data = request.data or None
        if not data:
            return Response({"Error": "Request data missing"},
                            status=S400)
        post_id = data.get("post_id") or None
        if not post_id:
            return Response({"Error":"invalid post id"},
                            status=S400)
        comments_objects =Comment.objects.filter(post=post_id).all()
        serial_comments = CommentSerializer(comments_objects, many=True).data
        return Response(serial_comments, status=S200)

class Like(APIView):
    def get(self, request):return Response(use_POST,status=S405)

    def post(self, request):
        token = request.headers.get('Authorization') or request.data["token"] or None
        username = auth.get_by(token=token) or None
        if not username:
            return Response(status=S401)
        data = request.data or None
        if not data:
            return Response({"Error": "Request data missing"},
            status=S400)

        user = Users.objects.filter(username=username).first()
        user_id = user.ID

        comment_data = data.get("comment") or None
        post_data = data.get("post") or None

        if not comment_data and not post_data:
            msg = "Comment or post data also required"
            return Response({"Error": msg}, status=S400)
        if comment_data:
            ID = comment_data.get("ID") or None
            action = comment_data.get("action") or None
            if not ID or not action:
                return Response({"Error":"ID, action required"},status=S400)

            comment = Comment.objects.filter(ID=ID).first()
            if not comment : return Response(f"comment for {ID}:{comment}", S400)
            if action == "like":
                if comment.dislikes.filter(ID=user.ID).exists():
                    comment.dislikes.remove(user)
                if not comment.likes.filter(ID=user.ID).exists():
                    comment.likes.add(user)

            elif action == "dislike":
                if comment.likes.filter(ID=user.ID).exists():
                    comment.likes.remove(user)
                if not comment.dislikes.filter(ID=user.ID).exists():
                    comment.dislikes.add(user)


            likes_usernames = list(comment.likes.values_list('username', flat=True))
            dislikes_usernames = list(comment.dislikes.values_list('username', flat=True))

        return Response(
            {
                "detail": f"Like processed successfully",
                "likes":likes_usernames,
                "dislikes":dislikes_usernames
            },
        status=S200)

class GetObjectById(APIView):
    def get(self, request):return Response(use_POST,status=S405)
    def post(self, request):
        result = get_object(request)
        if result[0]:
            return Response(result[1], S200)
        return Response(result[1], S404)
class UpdateByID(APIView):
    def get(self, request):return Response(use_POST,status=S405)
    def post(self, request):
        result = get_object(request)
        if not result[0]:
            return Response(result[1], S404)
        obj = result[3]
        new = result[2]
        if not new:
            return Response({"issue":f"new data {new}"}, S400)

        if obj.__class__ == Users:
            pass


        return Response( S200)

