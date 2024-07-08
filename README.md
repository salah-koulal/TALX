
# Social Media Application

This is a social media application built using Django, MySQL, and SQLAlchemy. It allows users to create profiles, connect with friends, post updates, and interact with others in a social networking environment.

## Features

- **User Authentication**: Secure user registration and authentication.
- **Profiles**: Users can create and manage their profiles with bio, profile picture, etc.
- **Friend Connections**: Users can send friend requests, accept or decline requests, and manage their friend list.
- **Posts**: Users can create posts, share updates, and like/comment on posts.
- **Messaging**: Private messaging functionality between users.
- **Search**: Search functionality to find other users and posts.

## Technologies Used

- **Django**: High-level Python web framework for rapid development and clean, pragmatic design.
- **MySQL**: Relational database management system for storing application data.
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapping (ORM) library for database interaction.

## Setup Instructions

### Prerequisites

- Python (3.6+)
- Django (`pip install django`)
- MySQL Server
- SQLAlchemy (`pip install sqlalchemy`)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**:

   - Create a MySQL database and configure credentials in `settings.py`:

     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'your_database_name',
             'USER': 'your_database_user',
             'PASSWORD': 'your_database_password',
             'HOST': 'localhost',  # Or your MySQL host
             'PORT': '3306',  # Or your MySQL port
         }
     }
     ```

   - Apply migrations to create database schema:

     ```bash
     python manage.py migrate
     ```

5. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

6. **Access the application**:

   Open a web browser and go to `http://127.0.0.1:8000/`.

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit pull requests with your improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

---

Adjust the `<repository_url>`, `<repository_directory>`, `your_database_name`, `your_database_user`, and `your_database_password` placeholders according to your actual project details. This `README.md` provides an overview of the project, setup instructions, technologies used, and guidance for contributors, ensuring clarity for anyone exploring or working with your social media application.
# Dinamo
https://www.youtube.com/watch?v=e1IyzVyrLSU
# Team 
https://www.youtube.com/watch?v=c-QsfbznSXI
