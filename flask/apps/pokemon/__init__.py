from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='./../../static')
app.secret_key = '\x024\xe6\x98\x8cq\x06mh\x90(4\xe6\xf5\xe9\xd6\xe4\x8f\x86\x91\x1f\xc0\xee\xaf'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

# the import was moved here to prevent circular dependencies between models.py and server.py
# ./manage.py -> import models
# ./models.py -> from __main__ import db
from apps.pokemon import models  # Module level not imported at top and unused skipcq: FLK-E402, PYL-W0611

# All the routes are moved to views.py
# ./manage.py -> import views
# ./models.py -> from __main__ import app, db
from apps.pokemon import views  # Module level not imported at top and unused skipcq: FLK-E402, PYL-W0611