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
