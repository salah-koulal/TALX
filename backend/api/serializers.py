from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import Profile, Post, LikePost, Comment, Following

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(
            email=clean_data["email"],
            password=clean_data["password"],
            username=clean_data["username"],
            first_name=clean_data["first_name"],
            last_name=clean_data["last_name"],
        )
        user_obj.save()
        Profile.objects.create(user=user_obj)
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    ##
    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data["username"], password=clean_data["password"]
        )
        if not user:
            raise ValidationError("user not found")
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "email", "username", "first_name", "last_name")
        read_only_fields = ("id",)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class FollowingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followed_user = UserSerializer(read_only=True)

    class Meta:
        model = Following
        fields = "__all__"
