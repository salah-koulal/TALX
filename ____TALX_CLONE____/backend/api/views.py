#backend/api/views.py
import jwt


from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, status, generics

from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta


from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
from .authentication import Authentication
######################  GLOBALS ################################

auth = Authentication()
x = {"username":"Kyoko",
     "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ikt5b2tvIiwiZXhwIjoxNzIxMTk0MjcxfQ.wlkL7OrId4K_yO7dBO2HRwjBQwC22rS5gf7H2sAEhrk"

     }
auth.cookies_session.append(x)
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
        } ,status=status.HTTP_200_OK)

class UserRegister(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    def post(self, request):
        return auth.register_user(request)

class getCSRFCookie(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrftoken': csrf_token})

#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"detail": "Please use POST to login."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):

        return auth.login_username(request)

class UserLogout(APIView):
    def get(self, request):
        return Response({"detail": "Please use POST to logout."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        return auth.logout_username(request)

class AddPost(APIView):
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
                                    status=status.HTTP_400_BAD_REQUEST)

                author = Users.objects.filter(username=username).first()
                serialized_user = author.to_dict()

                post_data["author"] = author
                post_obj = Post(**post_data)
                post_obj.save()
                saved_post = post_obj
                serialized_post = PostSerializer(saved_post).data
                saved_post = Post.objects.filter(author=author).first()
                return Response(saved_post.to_dict() ,
                                status=status.HTTP_200_OK)
        return Response(
                        status=status.HTTP_400_BAD_REQUEST)