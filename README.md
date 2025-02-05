# Pokedex-App 
This project intends to provide with a Pokedex-like UI and its relevant CRUD operations. On top of that, [pokeapi](https://pokeapi.co/) can be used here to feed the creation of new entries.

The project was structured as follows, inside a path of folders **flask/apps/pokemon/**, there are the following files and folders:
- **models.py**: contains ORM for database schema
- **views.py:** contains application logic i.e the response the apps returns
- **./templates/**: contains Jinja html templates
- **forms.py**: contains flask_wtf forms

In addition to this, I've implemented **manage.py** file for common database migration commands and running server commands.
For database, I have used SQlite. Instead of using raw SQL queries I have chosen to use SQLAlchemy to understand ORM database model.


## How to use:    
- Clone this  [repository](https://github.com/aerosback/pokedex-app)  
- Run the following to build docker containers (if they do not exist) and then run them. Do as follows to run them as a dettached process: 
    `docker compose up -d` 
- Or if you want to run this watching the output of the current underlying process:
    `docker compose up` 
- to stop running containers do the following:   
    `docker compose down`

## How to access via browser the web app locally: 

- Open your browser and type:   
    `http://localhost:8003/`

## Database Schema
![enter image description here](https://github.com/aerosback/pokedex-app/tree/main/flask/assets/database_schema.png)

