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
{
    "email": "alfaresZizo@example.com",
    "username": "zyead",
    "password": "zizo22fares24@x",
    "first_name": "zizo",
    "last_name": "elfares"
}
# login
 {
    "username": "Kyoko",
    "password": "passwordx123"
}
{
    "username": "zyead",
    "password": "zizo22fares24@x"
}

curl -X POST http://127.0.0.1:8000/api/login/ -d "username=Kyoko" -d "password=passwordx123"

{
    "token":

    "post":{
    }
}