from flask import Flask
from database.database import db
from api import account, user, ads, log, jwt, json
from processing import babel

"""
Create an application object and load configurations from file
"""
app = Flask(__name__)
app.config.from_pyfile('config.py')

"""
Bind instances to the current app which include database, 
babel processing, JWT tokenizing and json formatting
"""
db.init_app(app)
babel.init_app(app)
jwt.init_app(app)
json.init_app(app)


"""
Create blueprints for url routing:
- https://<domain_name.xyz>/
- https://<domain_name.xyz>/user
- https://<domain_name.xyz>/logging
"""

app.register_blueprint(account)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(ads)
app.register_blueprint(log, url_prefix='/logging')

with app.app_context():
   db.create_all()      # Initialize database instance
