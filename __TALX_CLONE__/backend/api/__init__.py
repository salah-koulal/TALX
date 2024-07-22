#backend/api/__init__.py
from rest_framework import status as S
from .validations import UserValidator, PostValidator, CommentValidator

userval = UserValidator()
postval = PostValidator()
comntval = CommentValidator()
S200 = S.HTTP_200_OK
S201 = S.HTTP_201_CREATED
S304 = S.HTTP_304_NOT_MODIFIED
S400 = S.HTTP_400_BAD_REQUEST
S401 = S.HTTP_401_UNAUTHORIZED
S405 = S.HTTP_405_METHOD_NOT_ALLOWED
S403 = S.HTTP_403_FORBIDDEN
S404 = S.HTTP_404_NOT_FOUND

