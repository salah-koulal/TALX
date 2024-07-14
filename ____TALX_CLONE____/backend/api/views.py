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
    return Response({"logged_users":auth.logged_users, "cookies_session":auth.cookies_session} ,status=status.HTTP_200_OK)

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
        return Response({"detail": "Please use POST to login."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):

        return auth.login_username(request)

class UserLogout(APIView):
    def get(self, request):
        return Response({"detail": "Please use POST to logout."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        return auth.logout_username(request)

