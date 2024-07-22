#backend/api/views.py
import jwt


from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions

from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta


from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
from .authentication import Authentication
from .__init__ import *
from .header import *
######################  GLOBALS ################################

auth = Authentication()
x = {"username":"Kyoko",
     "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ikt5b2tvIiwiZXhwIjoxNzIxMTk0MjcxfQ.wlkL7OrId4K_yO7dBO2HRwjBQwC22rS5gf7H2sAEhrk"

     }
auth.cookies_session.append(x)

###
use_POST = {"detail": f"Please use POST ."}
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
    auth.reload()
    return Response({
        "logged_users":auth.logged_users, "cookies_session":auth.cookies_session
        } ,status=S200)

class UserRegister(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    def post(self, request):
        return auth.register_user(request)

class getCSRFCookie(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrftoken': csrf_token})

#         return Response({'detail': 'Invalid credentials'}, status=S401)
class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):return Response(use_POST,status=S405)

    def post(self, request):

        return auth.login_username(request)

class UserLogout(APIView):
    def get(self, request):
        return Response({"detail": "Please use POST to logout."},
                        status=S405)

    def post(self, request):
        return auth.logout_username(request)

class AddPost(APIView):
    def get(self, request): return Response(use_POST, status=S405)
    def post(self, request):
        required = {"token", "post"}
        req_post = {"author", "content", "type"}

        if request  and request.data and required.issubset(request.data.keys()):
            post_data = request.data["post"]
            print(f"\n\n\n :: from AddPost >>  {post_data} ")
            token    = request.data.get("token")
            username =  auth.get_by(token)
            if auth.is_logged(token=token):

                if not req_post.issubset(post_data.keys()):
                    return Response([{"Error":f"{req_post} are required"}, req_post,request.data],
                                    status=S400)

                author = Users.objects.filter(username=username).first()
                serialized_user = author.to_dict()

                post_data["author"] = author
                post_obj = Post(**post_data)
                post_obj.save()
                saved_post = post_obj
                serialized_post = PostSerializer(saved_post).data
                saved_post = Post.objects.filter(author=author).first()
                return Response(saved_post.to_dict() ,
                                status=S200)
        return Response(status=S400)
class AddComment(APIView):
    def get(self, request):return Response(use_POST, status=S405)

    def post(self, request):
        if not request or not  request.data :
            return Response(status=S400)
        data = request.data["comment"] or None
        token = request.headers.get('Authorization') or request.data["token"] or None

        if not data or not token:

            return Response({"messing":"asdas"} , status=S400)
        author_name = auth.get_by(token=token)
        if not author_name:
            return Response(status=S401)

        author = Users.objects.filter(username=author_name).first()
        if not author:
            return Response({"Error":f"{author_name} not found"})


        post_id = data["post_id"] or None
        content = data["content"] or None

        if not post_id or not content:
                return Response({"messing":"comment and post_id required "},
                                status=S400)

        post_obj = Post.objects.filter(ID=post_id).first()
        if not post_obj:
            return Response({"Error":f"{post_id} is not a valid id "},
                            status=S304)
        comment ={
            "author":author, "post":post_obj, "content":content
        }
        comment_obj = Comment(**comment)
        comment_obj.save()
        ser_comment = CommentSerializer(comment_obj).data
        return Response(ser_comment, status=S201)




class GetAllByToken(APIView):
    def get(self, request): return Response(use_POST, status=S405)

    def post(self, request):
        token = request.headers.get('Authorization') or request.data["token"] or None
        username = auth.get_by(token=token) or None
        if not username:
            return Response(status=S401)
        data = request.data or None
        if not data:
            return Response({"Error": "Request data missing"},
                            status=S400)
        response_obj = {}
        msg = ""
        user = Users.objects.filter(username=username).first()
        for key in data.keys():
            if key == "token":
                continue
            cls_name = key.lower().strip().capitalize()
            if cls_name  in classes.keys():
                if cls_name in ["Comment", "Post"]:
                    all_objs=classes[cls_name].objects.filter(author=user.ID).all()
                else:
                    all_objs=classes[cls_name].objects.filter(username=username).all()
                # serial_objs=cls_serializers[cls_name](all_objs, many=True).data
                serial_objs = [obj.to_dict() for obj in all_objs]
                response_obj[key] = serial_objs

            else:
                if len(msg) > 0:
                    msg += ", "
                else:
                    msg += "can't find "
                msg += f"{key}"

        if msg == "":
            msg = None


        return Response({"data":response_obj, "issues":msg},
                        status=S200 )

class PostComments(APIView):
    def get(self, request): return Response(use_POST,status=S405)

    def post(self, request):
        token = request.headers.get('Authorization') or request.data["token"] or None
        username = auth.get_by(token=token) or None
        if not username:
            return Response(status=S401)
        data = request.data or None
        if not data:
            return Response({"Error": "Request data missing"},
                            status=S400)
        post_id = data.get("post_id") or None
        if not post_id:
            return Response({"Error":"invalid post id"},
                            status=S400)
        comments_objects =Comment.objects.filter(post=post_id).all()
        serial_comments = CommentSerializer(comments_objects, many=True).data
        return Response(serial_comments, status=S200)

class Like(APIView):
    def get(self, request):return Response(use_POST,status=S405)

    def post(self, request):
        token = request.headers.get('Authorization') or request.data["token"] or None
        username = auth.get_by(token=token) or None
        if not username:
            return Response(status=S401)
        data = request.data or None
        if not data:
            return Response({"Error": "Request data missing"},
            status=S400)

        user = Users.objects.filter(username=username).first()
        user_id = user.ID

        comment_data = data.get("comment") or None
        post_data = data.get("post") or None

        if not comment_data and not post_data:
            msg = "Comment or post data also required"
            return Response({"Error": msg}, status=S400)
        if comment_data:
            ID = comment_data.get("ID") or None
            action = comment_data.get("action") or None
            if not ID or not action:
                return Response({"Error":"ID, action required"},status=S400)

            comment = Comment.objects.filter(ID=ID).first()
            if not comment : return Response(f"comment for {ID}:{comment}", S400)
            if action == "like":
                if comment.dislikes.filter(ID=user.ID).exists():
                    comment.dislikes.remove(user)
                if not comment.likes.filter(ID=user.ID).exists():
                    comment.likes.add(user)

            elif action == "dislike":
                if comment.likes.filter(ID=user.ID).exists():
                    comment.likes.remove(user)
                if not comment.dislikes.filter(ID=user.ID).exists():
                    comment.dislikes.add(user)


            likes_usernames = list(comment.likes.values_list('username', flat=True))
            dislikes_usernames = list(comment.dislikes.values_list('username', flat=True))

        return Response(
            {
                "detail": f"Like processed successfully",
                "likes":likes_usernames,
                "dislikes":dislikes_usernames
            },
        status=S200)

class GetObjectById(APIView):
    def get(self, request):return Response(use_POST,status=S405)
    def post(self, request):
        result = get_object(request)
        if result[0]:
            return Response(result[1], S200)
        return Response(result[1], S404)

class UpdateByID(APIView):
    def get(self, request):
        return Response({"detail": "Use POST method"}, status=S.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        token = request.headers.get('Authorization') or request.data.get('token')
        if not token:
            return Response({"detail": "Authentication token is missing"}, status=S.HTTP_401_UNAUTHORIZED)

        username = auth.get_by(token=token)
        if not username or not auth.is_logged(token=token):
            return Response({"detail": "Authentication failed"}, status=S.HTTP_401_UNAUTHORIZED)

        password = request.data.get('password')
        if not password:
            return Response({"detail": "Password is required"}, status=S.HTTP_400_BAD_REQUEST)

        result = get_object(request)
        if not result[0]:
            return Response({"detail": result[1]}, S404)
        obj = result[3]
        new = result[2]
        if not new:
            return Response({"issue": f"New data {new}"},S400)

        if obj.__class__.__name__ == 'Users':
            if obj.username != username:
                return Response({"detail": "You can only update your own data"}, S403)
            if not auth.authenticate(username=username, password=make_password(password)):
                return Response({"detail": "Password incorrect"}, S401)
            update_result = obj.update_user(new)
        elif obj.__class__.__name__ == 'Comment':
            if obj.author.username != username:
                return Response({"detail": "You can only update your own comments"},S403)
            update_result = obj.update_comment(new)
        elif obj.__class__.__name__ == 'Post':
            if obj.author.username != username:
                return Response({"detail": "You can only update your own posts"}, S403)
            update_result = obj.update_post(new)
        else:
            return Response({"detail": "Unsupported class for update"}, S400)

        if not update_result[0]:
            return Response({"detail": update_result[1]}, S400)

        return Response(update_result[1], S200)

class DeleteByID(APIView):
    def get(self, request):
        return Response({"detail": "Use POST method"}, status=S405)

    def post(self, request):
        token = request.headers.get('Authorization') or request.data.get('token')
        if not token:
            return Response({"detail": "Authentication token is missing"}, status=S401)

        username = auth.get_by(token=token)
        if not username or not auth.is_logged(token=token):
            return Response({"detail": "Authentication failed"}, status=S401)

        password = request.data.get('password')
        if not password:
            return Response({"detail": "Password is required"}, status=S400)

        result = get_object(request)
        if not result[0]:
            return Response({"detail": result[1]}, status=S404)
        obj = result[3]

        if obj.__class__.__name__ == 'Users':
            if obj.username != username:
                return Response({"detail": "You can only delete your own data"}, status=S403)
            if not auth.authenticate(username=username, password=make_password(password)):
                return Response({"detail": "Password incorrect"}, status=S401)
            obj.delete()
        elif obj.__class__.__name__ == 'Comment':
            if obj.author.username != username:
                return Response({"detail": "You can only delete your own comments"}, status=S403)
            obj.delete()
        elif obj.__class__.__name__ == 'Post':
            if obj.author.username != username:
                return Response({"detail": "You can only delete your own posts"}, status=S403)
            obj.delete()
        else:
            return Response({"detail": "Unsupported class for deletion"}, status=S400)

        return Response({"detail": "Deleted successfully"}, status=S200)