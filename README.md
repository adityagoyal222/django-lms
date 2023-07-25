# Django LMS

Django LMS is a Learning Management System using the framework, you guessed it right, Django. The system gives teachers and students a simple platform to upload resources and assignments.

# Motivation
The project started as a challenge to improve and test my knowledge of Django. The initial version of this project was created within 5 days.

# Tech/Framework Used
* Python
* Django
* HTML
* CSS
* Bootstrap

# Features
This platform is fairly simple yet provides most of the necessary features required in a Learning Management System. It uses Django's MTV architecture.
* Signup
* Login
* Logout
* Course Creation
* Course Deletion
* Assignment Creation
* Assignment Submission
* Assignment Deletion
* Delete Submission
* Grade Submission
* Resource Creation
* Resource Deletion
* User Profile

# Installation process
The installation process involves cloning this repository, installing mysql-server, running this website and installing tailwind whic is used for styling.
1. Fork this repository then clone it to your local machine.
2. Install mysql-server and create a database named 'django_lms'. For those using linux, you can follow this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04) to install mysql-server.
3. Note the password you have assigned to the root user you will need it later.
4. Open the project in your favorite code editor 
5. Delete the existing virtualenv folder then ,open terminal then create a virtual Environment using the command `python3 -m venv virtualenv`.
6. Activate the virtual environment using the command `source virtualenv/bin/activate`.
7. Install the requirements using the command `pip install -r requirements.txt`.
8. Open the settings.py file in the django_lms folder of  the project and change the password in the database dictionary to the password you assigned to the root user. 

    this is how the database dictionary should look like after changing the password.
    ```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_lms',
        'USER': 'root',
        'PASSWORD': 'your_password_type_here',
        'HOST': 'localhost',
        'PORT': '3306',
    }
    
9. Run the command `python manage.py makemigrations` then `python manage.py migrate` to create the tables in the database.
10. Then install tailwind for django using this process:
        * python -m pip install django-tailwind[reload]
        * python manage.py tailwind install - ensures tailwind dependencies are installed

11. finally to run the project use the command `python manage.py tailwind start` in one terminal then open another terminal in the same directory and ensure you are in the virtual environment by typing `source virtualenv/bin/activate`. then the command : `python manage.py runserver` to run the website.
12. Open your browser and type `localhost:8000` in the address bar to view the website.