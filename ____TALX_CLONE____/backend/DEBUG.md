# running  server output
```sh
mohamed@DESKTOP-S296B4S /mnt/c/Users/Active/Desktop/Coding/Short_Specializations/Portfolio_project/TALX/____TALX_CLONE____/backend
 % ./manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 17, 2024 - 07:20:09
Django version 4.2.10, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

Method Not Allowed: /api/post/
[17/Jul/2024 07:20:12] "GET /api/post/ HTTP/1.1" 405 5590



 :: from AddPost >>  {'author': 'Kyoko', 'content': 'asdsjalskd sd askl sad jasl djlas ', 'image': None, 'type': 'info'}
Internal Server Error: /api/post/
Traceback (most recent call last):
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/fields/__init__.py", line 2688, in to_python
    return uuid.UUID(**{input_form: value})
  File "/usr/lib/python3.8/uuid.py", line 171, in __init__
    raise ValueError('badly formed hexadecimal UUID string')
ValueError: badly formed hexadecimal UUID string

During handling of the above exception, another exception occurred:

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
  File "/mnt/c/Users/Active/Desktop/Coding/Short_Specializations/Portfolio_project/TALX/____TALX_CLONE____/backend/api/views.py", line 102, in post
    saved_post = Post.objects.filter(author="Kyoko").first()
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/query.py", line 1436, in filter
    return self._filter_or_exclude(False, args, kwargs)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/query.py", line 1454, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/query.py", line 1461, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1546, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1577, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1492, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/sql/query.py", line 1319, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/lookups.py", line 27, in __init__
    self.rhs = self.get_prep_lookup()
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/fields/related_lookups.py", line 166, in get_prep_lookup
    self.rhs = target_field.get_prep_value(self.rhs)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/fields/__init__.py", line 2672, in get_prep_value
    return self.to_python(value)
  File "/home/mohamed/.local/lib/python3.8/site-packages/django/db/models/fields/__init__.py", line 2690, in to_python
    raise exceptions.ValidationError(
django.core.exceptions.ValidationError: ['“Kyoko” is not a valid UUID.']
[17/Jul/2024 07:20:

```


# Base  , Post and AddPost classes

```py
class Base(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict['ID'] = str(new_dict['ID'])
        if  "created_date" in new_dict:
            new_dict['created_date'] = new_dict['created_date'].strftime(time_format)
        if  "updated_date" in new_dict:
            new_dict['updated_date'] = new_dict['updated_date'].strftime(time_format)
        new_dict.pop('_state', None)
        if 'date_joined' in new_dict:
            new_dict['date_joined'] = new_dict['date_joined'].strftime(time_format)
        if 'password' in new_dict:
            # new_dict['password'] = make_password(new_dict['password'])
            new_dict.pop("password")
        if 'user_id' in new_dict:
            new_dict['user_id'] = str(new_dict['user_id'])
        return new_dict

        return new_dict

    class Meta:
        abstract = True

class Post(Base):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_image/", null=True, blank=True)
    type = models.CharField(
        max_length=4,  choices=[("meme", "Meme"), ("info", "Info")]
    )
```