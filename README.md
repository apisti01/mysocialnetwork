# MySocialNetwork

MySocialNetwork is a Django-based social networking platform where users can create profiles, make friends, share posts, like and comment on posts.
Created as a project for the course PPM at University of Florence.

## Features

- **User Registration and Authentication**: Users can register and log in to the platform.
- **User Profiles**: Users can create and update their profiles, including profile pictures.
- **Friend Requests**: Users can send and accept friend requests.
- **Posts**: Users can create, delete, and view posts.
- **Likes and Comments**: Users can like and comment on posts.
- **News Feed**: Users can see a feed of all posts and a separate feed of posts from friends.

## Installation


### Setting Up the Project

1. **Clone the repository:**

   ```sh
   git clone https://github.com/apisti01/mysocialnetwork.git
   cd mysocialnetwork
    ```
2. **Create a virtual environment:**

    create a virtual environment with your favorite tool with python-3.9.19

3. **Install the dependencies:**

   ```sh
    pip install -r requirements.txt
    ```
4. **Set up the database:**

   create a sqlite3 database in the root folder of the project with the name `db.sqlite3`

5. **Create a `.env` file in the root folder of the project with the following content:**

   ```sh
   SECRET_KEY=your_secret_key
   DEBUG=True
   '''

6. **Run migrations:**

   ```sh
   python manage.py makemigrations
   python manage.py migrate
    ```
7. **Collect static files:**

   ```sh
   python manage.py collectstatic
    ```
8. **Run the development server:**

   ```sh
   python manage.py runserver
    ```
Project will be available at `http://127.0.0.1:8000/`.

## Deployment
The project has been deployed on Railway and can be accessed [here](https://mysocialnetwork-production.up.railway.app/).

### Thank you for using MySocialNetwork!


