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
    def reload(self):
        self.logged_users = [cookie["username"] for cookie in self.cookies_session]

    def new_token(self, username: str, exp: int) -> str:
        secret_key = "HORIZONS-SECRET-KEY"

        payload = {
            "username": username,
            "exp": datetime.utcnow() + timedelta(days=exp)
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')

    def register_user(self, request):

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

    def login_username(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = Users.objects.filter(username=username).first()
        if user is None:
            return Response({'detail': f'{username} does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
        print(f" \n\n\n From Login  {user.password} {make_password(password) == user.password} \n\n\n")
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
