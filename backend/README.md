## To load dummy data to you app

1. Run the following commands:
    ```
        cd backend
        python manage.py shell
    ```
2. Run the following script:
   ```
   from django.contrib.auth.models import User
    from django.utils import timezone

    users = [
        {
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "john123",
            "date_joined": timezone.now()
        },
        {
            "username": "janedoe",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@example.com",
            "password": "jane123",
            "date_joined": timezone.now()
        },
        {
            "username": "alicesmith",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alicesmith@example.com",
            "password": "alice123",
            "date_joined": timezone.now()
        },
        {
            "username": "bobwilson",
            "first_name": "Bob",
            "last_name": "Wilson",
            "email": "bobwilson@example.com",
            "password": "bob123",
            "date_joined": timezone.now()
        },
        {
            "username": "emmabrown",
            "first_name": "Emma",
            "last_name": "Brown",
            "email": "emmabrown@example.com",
            "password": "emma123",
            "date_joined": timezone.now()
        },
        {
            "username": "michaelgreen",
            "first_name": "Michael",
            "last_name": "Green",
            "email": "michaelgreen@example.com",
            "password": "michael123",
            "date_joined": timezone.now()
        }
    ]

    for user_data in users:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.date_joined = user_data['date_joined']
        user.save()
        print(f"Created user: {user.username}")

    print("All users created successfully!")
   ```

3. Now Run this command to load data from fixture
    ```
    python manage.py loaddata initial_fixture
    ```
