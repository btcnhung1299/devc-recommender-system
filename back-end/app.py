from flask import Flask
from db_model import db
from api import account, user, ads, log, jwt, json
from helper import babel
from db_model import save_to_db

# Create an instance of flask server
app = Flask(__name__)

# Config
app.config.from_pyfile('config.py')

# Pass app instance
db.init_app(app)
babel.init_app(app)
jwt.init_app(app)
json.init_app(app)

# Create blueprints
app.register_blueprint(account)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(ads)
app.register_blueprint(log, url_prefix='/logging')

# Init database
with app.app_context():
   db.create_all()
