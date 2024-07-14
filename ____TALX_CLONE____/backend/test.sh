#!/bin/bash

curl -X POST http://127.0.0.1:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{"email": "usery@example.com",
"username": "yusery_",
"password": "passwordx123"}'


# register
{
    "email": "Kyoko-sun@example.com",
    "username": "Kyoko",
    "password": "passwordx123",
    "first_name": "first_name",
    "last_name": "last_name"
}
# login
 {
    "username": "Kyoko",
    "password": "passwordx123"
}
curl -X POST http://127.0.0.1:8000/api/login/ -d "username=Kyoko" -d "password=passwordx123"