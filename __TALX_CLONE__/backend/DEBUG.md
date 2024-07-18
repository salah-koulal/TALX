output
```sh
System check identified no issues (0 silenced).
July 18, 2024 - 21:48:59
Django version 4.2.10, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

/mnt/c/Users/Active/Desktop/Coding/Short_Specializations/Portfolio_project/Xtwittes/__TALX_CLONE__/backend/api/views.py changed, reloading.
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 18, 2024 - 21:53:31
Django version 4.2.10, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

Method Not Allowed: /api/get_all/
[18/Jul/2024 21:53:31] "GET /api/get_all/ HTTP/1.1" 405 6958
Internal Server Error: /api/get_all/
Traceback (most recent call last):
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/views/decorators/csrf.py", line 56, in wrapper_view
    return view_func(*args, **kwargs)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/views/generic/base.py", line 104, in view
    return self.dispatch(request, *args, **kwargs)
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/views.py", line 509, in dispatch
    response = self.handle_exception(exc)
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/views.py", line 469, in handle_exception
    self.raise_uncaught_exception(exc)
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/views.py", line 480, in raise_uncaught_exception
    raise exc
  File "/home/mohamed/.local/lib/python3.8/site-packages/rest_framework/views.py", line 506, in dispatch
    response = handler(request, *args, **kwargs)
  File "/mnt/c/Users/Active/Desktop/Coding/Short_Specializations/Portfolio_project/Xtwittes/__TALX_CLONE__/backend/api/views.py", line 205, in post
    serial_objs = [obj.to_dict() for obj in all_objs]
TypeError: 'method' object is not iterable
[18/Jul
```
code
```py
class GetAllByToken(APIView):
    def get(self, request):
        return Response({"detail": "Please use POST to like."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def post(self, request):
        token = request.headers.get('Authorization') or request.data["token"] or None
        username = auth.get_by(token=token) or None
        if not username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data or None
        if not data:
            return Response({"Error": "Request data missing"},
                            status=status.HTTP_400_BAD_REQUEST)
        response_obj = {}
        msg = ""
        user = Users.objects.filter(username=username).first()
        for key in data.keys():
            if key == "token":
                continue
            cls_name = key.lower().strip().capitalize()
            if cls_name  in classes.keys():
                if cls_name in ["Comment", "Post"]:
                    all_objs=classes[cls_name].objects.filter(author=user.ID).all
                else:
                    all_objs=classes[cls_name].objects.filter(username=username).all
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
                        status=status.HTTP_200_OK )
```
request
```json
{
"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ikt5b2tvIiwiZXhwIjoxNzIxMTk0MjcxfQ.wlkL7OrId4K_yO7dBO2HRwjBQwC22rS5gf7H2sAEhrk",

"comment": {

    "ID": "a140162a-cbc0-408a-a843-84469f621a55",
    "action":"like"
    },

"comment1": {

    "ID": "a140162a-cbc0-408a-a843-84469f621a55",
    "action":"like"
    },

"comment2": {

    "ID": "a140162a-cbc0-408a-a843-84469f621a55",
    "action":"like"
    }
}
```