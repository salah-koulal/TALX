from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
    PostSerializer,
    LikePostSerializer,
    ProfileSerializer,
    CommentSerializer,
    FollowingSerializer,
)
from .models import Profile, Post, LikePost, Comment, Following, AppUser
from rest_framework import permissions, status, generics
from .validations import custom_validation, validate_email, validate_password


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    ##
    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    ##
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)


# add permission classes later
class PostsView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ProfilesView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user__username"
    lookup_url_kwarg = "username"


class PostCommentsView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        queryset = Comment.objects.filter(post=post_id)
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(post=post)


class CommentsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikePostView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikePostSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        queryset = LikePost.objects.filter(post=post_id)
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(post=post)


class FollowUserView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowingSerializer

    def perform_create(self, serializer):
        followed_user = get_object_or_404(AppUser, id=self.kwargs["username"])
        serializer.save(followed_user=followed_user)


class FollowingView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowingSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        user_id = AppUser.objects.filter(username=username)
        queryset = Following.objects.filter(user=user_id)
        return queryset
