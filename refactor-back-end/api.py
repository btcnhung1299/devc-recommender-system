from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jti, get_raw_jwt
from flask_json import FlaskJSON, json_response

import database.views as views


"""Register blueprints for url routing
"""
account  = Blueprint('account', __name__) 
user     = Blueprint('user', __name__)
ads      = Blueprint('ads', __name__)
log      = Blueprint('logging', __name__)


"""Create json formatter
"""
json     = FlaskJSON()
jwt      = JWTManager()
blacklist_tokens = set()


@jwt.token_in_blacklist_loader
def is_expired_token(token):
   try:
      jti = token['jti']
   except:
      return True
   return jti in blacklist_tokens


@account.route('/register', methods=['POST'])
def register(): 
   try:
      views.User.init_from_request(request.json)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, message='Successfully registered')


@account.route('/login', methods=['POST'])
def login():
   """If user provides a valid account information, create an access
   token which expired in 1 day using user ID as identity.
   A newly provided access token must be removed from blacklist tokens of
   last sessiong.
   """
   try:
      phone                = request.json['phone']
      password             = request.json['password']
      user_id, user_name   = views.User.authenticate(phone, password)
   except Exception as error:
      return json_response(status_=404, error=str(error))

   expires        = timedelta(days=1)
   access_token   = create_access_token(identity=user_id, expires_delta=expires, fresh=True)
   
   try:
      access_jti  = get_jti(access_token)
      if access_jti in blacklist_tokens:
         blacklist_tokens.remove(access_jti)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, username=user_name, access_token=access_token)


@account.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
   jti      = get_raw_jwt()['jti']
   blacklist_tokens.add(jti)
   return json_response(status_=200, message='Successfully logged out')

