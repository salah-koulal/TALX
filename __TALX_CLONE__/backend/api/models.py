from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django.contrib.auth.hashers import make_password
from .__init__ import userval, postval, comntval

time_format = "%Y-%m-%dT%H:%M:%S.%f"

class Base(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # def update(self, new=None):
        # self.updated_date = datetime.now()
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict['ID'] = str(new_dict['ID'])
        if "created_date" in new_dict:
            new_dict['created_date'] = new_dict['created_date'].strftime(time_format)
        if "updated_date" in new_dict:
            new_dict['updated_date'] = new_dict['updated_date'].strftime(time_format)
        new_dict.pop('_state', None)
        if 'date_joined' in new_dict:
            new_dict['date_joined'] = new_dict['date_joined'].strftime(time_format)
        if 'password' in new_dict:
            new_dict.pop("password")
        if 'user_id' in new_dict:
            new_dict['user_id'] = str(new_dict['user_id'])
        return new_dict

    class Meta:
        abstract = True

class Users(Base, User):
    def update_user(self, data_obj=None):
        if not data_obj:
            return (False, "No data to update")

        result = userval.all(data_object=data_obj, all_required=False)
        if not result[0]:
            return result

        clean_data = result[1]
        similar_val_ky = []

        for key, value in clean_data.items():
            current_value = getattr(self, key, None)
            if key == "password":
                value = make_password(value)

            if current_value == value:
                similar_val_ky.append(key)
                continue

            setattr(self, key, value)

        if len(similar_val_ky) == len(clean_data):
            return (False, ", ".join(similar_val_ky) + " are the same")

        self.updated_date = datetime.now()
        self.save()
        return (True, self.to_dict())

    def __str__(self):
        return self.username
class Profile(Base):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to="profile_images",
        default="profile_images/blank-profile-picture.png",
    )
    def display(self):
        display_data =  {
            "username":self.user.username,
            "first_name":self.user.first_name,
            "last_name":self.user.last_name,
            "last_login":self.user.last_login,
            "is_active":self.user.is_active,
        }
        return True , display_data
    def __str__(self):
        return self.user.username

class Post(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_image/", null=True, blank=True)
    type = models.CharField(
        max_length=4, choices=[("meme", "Meme"), ("info", "Info")]
    )
    likes = models.ManyToManyField(
        Users, related_name="liked_posts", blank=True
    )
    dislikes = models.ManyToManyField(
        Users, related_name="disliked_posts", blank=True
    )
    def update_post(self, data=None):
        if not data:
            return (False, "No data to update")

        result = postval.all(data_obj=data, all_required=False)
        if not result[0]:
            return result

        clean_data = result[1]
        similar_val_ky = []

        for key, value in clean_data.items():
            if getattr(self, key) == value:
                similar_val_ky.append(key)
                continue
            setattr(self, key, value)

        if len(similar_val_ky) == len(clean_data.keys()):
            return (False, f"{', '.join(similar_val_ky)} are the same")

        self.updated_date = datetime.now()
        self.save()
        return (True, self.to_dict())

    def __str__(self):
        return f"{self.author.username}'s post"


class Comment(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    likes = models.ManyToManyField(
        Users, related_name="liked_comments", blank=True
    )
    dislikes = models.ManyToManyField(
        Users, related_name="disliked_comments", blank=True
    )
    def update_comment(self, data=None):
        if not data:
            return (False, "No data to update")

        result = comntval.all(data_obj=data, all_required=False)
        if not result[0]:
            return result

        clean_data = result[1]
        similar_val_ky = []

        for key, value in clean_data.items():
            if getattr(self, key) == value:
                similar_val_ky.append(key)
                continue
            setattr(self, key, value)

        if len(similar_val_ky) == len(clean_data.keys()):
            return (False, f"{', '.join(similar_val_ky)} are the same")

        self.updated_date = datetime.now()
        self.save()
        return (True, self.to_dict())



    def __str__(self):
        return f"{self.author.username}'s comment on {self.post}"

class Following(Base):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="followers"
    )

    class Meta:
        unique_together = ("user", "followed_user")

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"

class Report(Base):
    REPORT_CHOICES = [
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('user', 'User')
    ]
    reported_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="reports_made")
    report_type = models.CharField(max_length=10, choices=REPORT_CHOICES)
    reported_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="reports")
    reported_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name="reports")
    reported_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name="reports_against")
    reason = models.TextField()

    def __str__(self):
        return f"Report by {self.reported_by.username} on {self.report_type}"
classes = {
    "Comment":Comment, "Users":Users, "Post":Post,
    "Following":Following, "Report":Report
}
