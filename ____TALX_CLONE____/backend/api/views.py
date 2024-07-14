#backend/api/views.py
import jwt

from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, status, generics
from .validations import custom_validation, validate_email, validate_password
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta

from .models import (
    Users, Post, Profile, LikePost, Comment, Following, make_password
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
from django.contrib.auth.hashers import make_password

######################  GLOBALS ################################
cookies_session = []


def new_token(username:str, exp:int) ->str:
    secret_key  = "HORIZONS-SECRET-KEY"

    payload = {
        "username":username,
        "exp":datetime.utcnow() + timedelta(days=exp)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')
def check_password(hashed:str, password:str) -> str:
    """ check hashed password with ="""
    return hashed == make_password(password)

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
    return Response({"logged_users":logged_users, "cookies_session":cookies_session} ,status=status.HTTP_200_OK)

class UserRegister(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    def post(self, request):
        # Validate the incoming data
        clean_data = custom_validation(request.data)

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
class getCSRFCookie(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrftoken': csrf_token})

# class UserLogin(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             serializer = UsersSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"detail": "Please use POST to login."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user =  Users.objects.filter(username=username).first()
        if user is None:
            return Response({'detail': f'{username} is not exist '}, status=status.HTTP_401_UNAUTHORIZED)
        print(f" \n\n\n From Login  {user.password} {make_password(password) == user.password} \n\n\n")
        if not authenticate(username=username, password=password):
            return Response({'detail': ' password incorrect  '}, status=status.HTTP_401_UNAUTHORIZED)

        token = new_token(username, 1)
        user_found = False
        # check if the user is already  log in
        for cookie in cookies_session:
            if cookie.get("username") == username:
                cookie["token"] = token
                user_found = True
                break

        if not user_found:
            cookies_session.append({"token": token, "username": username})

        profiles = Profile.objects.filter(user=user).first()
        serial_data = ProfileSerializer(profiles).data
        # login(request, user)
        # logout(request)
        # serial_data["token"] = token
        return Response((serial_data, token), status=status.HTTP_200_OK)


class UserLogout(APIView):
    def get(self, request):
        return Response({"detail": "Please use POST to logout."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        username = request.data.get("username")
        logged_users = [cookie["username"] for cookie in cookies_session]

        if username:
            if username in logged_users:
                for cookie in cookies_session:
                    if cookie["username"] == username:
                        cookies_session.remove(cookie)
                        return Response({"detail": f"{username} logged out"}, status=status.HTTP_200_OK)
                # This block is theoretically unreachable due to previous check
                return Response({"detail": f"No active session found for {username}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Return a response if the username is not in logged_users
                return Response({"detail": f"{username} is not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return a response if no username is provided in the request
            return Response({"detail": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)
