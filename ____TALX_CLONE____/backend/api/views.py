#backend/api/views.py
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


class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        clean_data = custom_validation(request.data)
        print(f"\n\n::   clean_data ${clean_data}   >>  \n\n")
        serializer = UsersSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                # Create and save the profile for the new user
                profile = Profile(user=user)
                profile.save()

                # Include profile data in the response
                user_data = serializer.data
                user_data['profile'] = ProfileSerializer(profile).data

                return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class getCSRFCookie(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrftoken': csrf_token})

class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
