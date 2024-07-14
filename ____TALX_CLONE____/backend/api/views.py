#backend/api/views.py
import jwt


from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, status, generics
from .validations import custom_validation, validate_email, validate_password
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta

from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
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

        return auth.login_username(request)

class UserLogout(APIView):
    def get(self, request):
        return Response({"detail": "Please use POST to logout."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        return auth.logout_username(request)

