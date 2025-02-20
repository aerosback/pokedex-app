from apps.pokemon import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    ###################################
    # Commands for database migrations:
    # $ python manage.py run_server
    # $ python manage.py db init
    # $ python manage.py db migrate
    # $ python manage.py db upgrade
    ###################################
    manager.run()

    app.run()