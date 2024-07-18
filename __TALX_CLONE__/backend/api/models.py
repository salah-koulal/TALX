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
        max_length=4, choices=[("meme", "Meme"), ("info", "Info")]
    )
    likes = models.ManyToManyField(
        Users, related_name="liked_posts", blank=True
    )
    dislikes = models.ManyToManyField(
        Users, related_name="disliked_posts", blank=True
    )

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
