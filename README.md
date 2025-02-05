# Pokedex-App 
This project  creating Pokedox that allows CRUD operations.

The project was structured as follows:
- **models.py**: contains ORM for database schema
- **views.py:** contains application logic i.e the response the apps returns
- **./templates/**: contains Jinja html templates
- **forms.py**: contains wtforms

In addition to this, I've implemented **manage.py** file for common database migration commands and running server commands.
For database, I have used SQlite. Instead of using raw SQL queries I have chosen to use SQLAlchemy to understand ORM database model.


## How to use:    
- Clone this  [repository](https://github.com/)  
- Run the following to start docker containers (images and containers are created if they are not already)  
`pip install -r requirement.txt`  
- to stop running containers do the following:   
`python manage.py run_server`

## Database Schema
![enter image description here](https://github.com/pokedexapp/flask/apps/pokemon/assets/database%20schema.png)

