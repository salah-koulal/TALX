# Talx - Tech-Focused Social Media App

Talx is a social media platform specializing in tech topics. Built with Django, React, SQLite, and Redux, it provides a space for tech enthusiasts to connect, share ideas, and discuss the latest in technology.

## Project Structure

The project is divided into two main folders:

- `backend/`: Contains the Django server code
- `frontend/`: Houses the React client application

## Backend

The backend is built with Django and uses SQLite as the database.

### Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the Django server:
   ```
   python manage.py runserver
   ```

## Frontend

The frontend is built with React and uses Redux for state management.

### Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

## Features

- User authentication
- Create and share tech-related posts
- Comment on posts
- Follow other users
- Trending topics in tech
- User profiles

## Technologies Used

- Backend:
  - Django
  - SQLite
  - Django REST Framework

- Frontend:
  - React
  - Redux
  - React Router
  - Axios

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit pull requests with your improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).