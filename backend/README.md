# Django-ToDo-API

# Introduction

A simple To-Do List App using Django, which contains the following REST APIs created using DRF (DjangoRestFramework):

  a. CREATE a todo item
  
  b. READ one todo item
  
  c. READ all todo items
  
  d. UPDATE a todo item
  
  e. DELETE a todo item





# Getting started

To run this app locally, follow the steps:

### Installation

Clone the repository to your local machine:

    $ git clone https://github.com/your-username/django-todo-app.git
    
Navigate to the project directory::

    $ cd django-todo-app

### Create a virtual environment :

  On Windows:
    
    $ venv\Scripts\activate
  On macOS/Linux:

    $ source venv/bin/activate
### Install dependencies using pip:

    $ pip install -r requirements.txt

    
### Database Setup

Apply migrations to set up the database:

    $ python manage.py migrate

Create a superuser account (admin) for managing the todo app:

    $ python manage.py createsuperuser

    
### Run the Application:

    $ python manage.py runserver

### Coverage report

![Default Home View](coverage-report-html.png?raw=true "Title")

