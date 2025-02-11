# Pokedex-App 
This project intends to provide with a Pokedex-like UI and its relevant CRUD operations.
On top of that, [PokeAPI](https://pokeapi.co/) was used here to feed the creation of new entries.

The project was designed having in mind a Domain Driven Design (DDD) focus and thus structured as follows.
Inside a path of folders **flask/apps/pokemon/**, there are the following files:
- **dtos/types.py**: contains data classes also known as data transfer classes, which allow us to separate concerns between models and CRUD business logic operations.
- **dtos/utils.py**: contains useful function for the above dataclasses.
- **constants.py**: contains constant read only values such as enumations or scalar values.
- **exceptions.py**: contains custom exceptions.
- **forms.py**: contains flask_wtf forms.
- **models.py**: contains ORM model classes for database schema.
- **apis.py**: contains api calls to external services.
- **queries.py**: contains read only database-related retrieval functions.
- **services.py**: contains read-and-write database-related functions.
- **views.py:** contains application logic i.e the response the apps returns
- **utils.py**: contains miscellaneous useful functions.
- **./templates/**: contains Jinja html templates


In addition to this, a **manage.py** file for common database migration commands and running server commands was implemented.
SQlite was the database technology employed. Instead of using raw SQL queries, SQLAlchemy was used here as an ORM database model.
Nginx served here as a reverse web proxy which is linked with the uwsgi process running flask application.

## Requirements:
- Docker Engine: [Here](https://docs.docker.com/engine/install/) you will find how to install it according to your Operating System.
- Docker Compose v2. [Here](https://docs.docker.com/compose/install/) you will find how to install it according to your Operating System.

## How to use:    
- Clone this  [repository](https://github.com/aerosback/pokedex-app)  
- Run the following to build docker containers (if they do not exist) and then execute them (as a dettached process, to not watch containers' output):<br />
    `docker compose up -d` 
- Or if you want to run this watching the output of the current underlying process:<br />
    `docker compose up` 
- To stop running containers do the following:<br />
    `docker compose down`
- To build or rebuild containers do the following:<br /> 
    `docker compose build`

## How to access via browser the web app locally: 

- Open your browser and type:   
    `http://localhost:8003/`

## Available Key Views or Operations:

- **/index**: Home landing page.
- **/add_pokemon**: on this page we can add a new pokemon entry. Besides, here we can search remotely on the PokeAPI service by typing the name of the pokemon we are about to search and then clicking the button "remote search".
- **/list**: A listing page which displays all available pokemon entries in our database.
- **/detail**: A page where all features of a pokemon as well as its picture are displayed.
- **/edit_pokemon**: A page where a pokemon's features can be edited and persisted into our database.
- **/delete_pokemon**: Not a page but an operation which can be performed when one is at the List View. It allow us to delete a single pokemon entry from our database.

## Database Schema
![enter image description here](https://github.com/aerosback/pokedex-app/blob/943e7f28a5c955e221f021e400332fe99e1f178c/flask/assets/database_schema.png)

