from flask import Flask

import api
import database.views as views
import processing

# Create an application object and load configurations from file
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Bind instances to the current app which include database, 
# babel processing, JWT tokenizing and json formatting
views.db.init_app(app)
api.json.init_app(app)
api.jwt.init_app(app)
processing.babel.init_app(app)

"""Create blueprints for url routing:
- https://<domain_name.xyz>/
- https://<domain_name.xyz>/user
- https://<domain_name.xyz>/event
"""
app.register_blueprint(api.account)
app.register_blueprint(api.user, url_prefix='/user')
app.register_blueprint(api.ads)
app.register_blueprint(api.events, url_prefix='/event')


with app.app_context():
   views.db.create_all()      # Initialize database instance
