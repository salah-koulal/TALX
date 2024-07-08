from django.urls import path
from . import views

urlpatterns = [
    path("register", views.UserRegister.as_view(), name="register"),
    path("login", views.UserLogin.as_view(), name="login"),
    path("logout", views.UserLogout.as_view(), name="logout"),
    path("user", views.UserView.as_view(), name="user"),
    path("profiles", views.ProfilesView.as_view(), name="profiles"),
    path(
        "profiles/<str:username>",
        views.ProfileView.as_view(),
        name="user-profile",
    ),
    path("posts", views.PostsView.as_view(), name="posts"),
    path("posts/<pk>", views.PostView.as_view(), name="post"),
    path(
        "posts/<post_id>/comments",
        views.PostCommentsView.as_view(),
        name="post-comments",
    ),
    path("comments/<pk>", views.CommentsView.as_view(), name="comments"),
    path(
        "posts/<post_id>/likes", views.LikePostView.as_view(), name="like-post"
    ),
    path(
        "users/<str:username>/follow",
        views.FollowUserView.as_view(),
        name="follow-user",
    ),
    path(
        "users/<str:username>/following",
        views.FollowingView.as_view(),
        name="following",
    ),
]
