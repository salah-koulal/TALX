#backend/api/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django.contrib.auth.hashers import make_password
time_format = "%Y-%m-%dT%H:%M:%S.%f"

class Base(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict['ID'] = str(new_dict['ID'])
        new_dict['created_date'] = new_dict['created_date'].strftime(time_format)
        new_dict['updated_date'] = new_dict['updated_date'].strftime(time_format)
        new_dict.pop('_state', None)
        if 'date_joined' in new_dict:
            new_dict['date_joined'] = new_dict['date_joined'].strftime(time_format)
        # if 'password' in new_dict:
            # new_dict['password'] = make_password(new_dict['password'])
        if 'user_id' in new_dict:
            new_dict['user_id'] = str(new_dict['user_id'])
        return new_dict

        return new_dict

    class Meta:
        abstract = True

class Users(Base, User):

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
        max_length=4,  choices=[("meme", "Meme"), ("info", "Info")]
    )
class LikePost(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username} like {self.post}"
class Comment(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    content = models.CharField(max_length=500)

class Following(Base):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        Users, on_delete= models.CASCADE, related_name="followers"
    )
    class Meta:
        unique_together = ("user", "followed_user")

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"