#backend/api/serializers.py
from rest_framework import serializers
from .models import (
   Base, Users, Profile, Post, LikePost, Comment, Following
    )



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