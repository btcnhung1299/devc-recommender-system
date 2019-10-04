# Import flask
from flask import Blueprint, request

# Import flask extensions
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jti, get_raw_jwt
from flask_json import FlaskJSON, json_response
from werkzeug.security import safe_str_cmp

# Import wrapper
from db_model import db, hash_password, User, Ad, AdEvent

# Import error handlers
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc

# Import standard libraries
import datetime

# Create instances of JWTManager and JSON
jwt = JWTManager()
json = FlaskJSON()

# Flask blueprints
account  = Blueprint('account', __name__) 
user     = Blueprint('user', __name__)
ads      = Blueprint('ads', __name__)
log      = Blueprint('logging', __name__)

# Init a blacklist to invalidate a token
blacklist_tokens = set()


# --------------------- HELPER FUNCTIONS --------------------
def authenticate(phone, password):
   try:
      user = db.session.query(User.user_id, User.password, User.name).\
                              filter(User.phone == phone).one()
      db_password = user.password
      password    = hash_password(password)
   except AttributeError:
      raise Exception('Inconsistent attributes query')
      return
   except:
      raise Exception('Wrong username or password')
      return

   if not safe_str_cmp(password, db_password):
      raise Exception('Wrong username or password')
      return
   
   return (user.user_id, user.name)

@jwt.token_in_blacklist_loader
def is_expired_token(token):
   try:
      jti = token['jti']
   except:
      return True

   if jti in blacklist_tokens:
      return True
   return False

# -------------------------- / ---------------------------
@account.route('/register', methods=['POST'])
def register():
   try:
      User.init_from_request(request.json)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, message='Successfully registered')


@account.route('/login', methods=['POST'])
def login():
   try:
      phone                = request.json['phone']
      password             = request.json['password']
      user_id, user_name   = authenticate(phone, password)
   except Exception as error:
      return json_response(status_=404, error=str(error))

   expires        = datetime.timedelta(days=1)
   access_token   = create_access_token(identity=user_id, \
                                        expires_delta=expires, fresh=True)
   
   try:
      access_jti  = get_jti(access_token)
      if access_jti in blacklist_tokens:
         blacklist_tokens.remove(access_jti)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, username = user_name, \
                        access_token=access_token)


@account.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
   jti      = get_raw_jwt()['jti']
   blacklist_tokens.add(jti)
   return json_response(status_=200, message='Successfully logged out')


# ------------------------- /user -------- ------------------
@user.route('/personal-profile', methods=['GET'])
@jwt_required
def get_user_profile(): 
   user_id        = get_jwt_identity()
   user           = User.query.get(user_id)
   if user == None:
      return json_response(status_=404, error='User not found')
   return json_response(status_=200, profile=user.get_profile())


@user.route('/edit', methods=['PUT'])
@jwt_required
def edit_user_profile():
   user_id        = get_jwt_identity()
   user           = User.query.get(user_id)
   if user == None:
      return json_response(status_=404, error='User not found')

   try:
      user.update_from_request(request=request.json)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, \
                        message='Succesfully updated profile')
  

# ------------------------- / ----------------------------
@ads.route('/post', methods=['POST'])
@jwt_required
def post():
   owner_id       = get_jwt_identity()
   try:
      Ad.init_from_request(owner_id=owner_id, request=request.json)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, message='Successfully posted')


@ads.route('/infor', methods=['GET'])
def get_ad_infor():
   adlist_id   = request.args.get('adlist_id')
   ad          = Ad.query.get(adlist_id)
   if ad == None:
      return json_response(status_=404, error='Item not found')

   try:
      infor       = ad.get_infor()
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, infor=infor)


@ads.route('/adlisting', methods=['GET'])
def display_ads():
   main_category_id  = request.args.get('main_category', type=int)
   page              = request.args.get('page', type=int)
   category_id       = request.args.get('category', type=int)
   region_id         = request.args.get('region', type=int)
   area_id           = request.args.get('area', type=int)
   min_price         = request.args.get('min_price', type=int)
   max_price         = request.args.get('max_price', type=int)
   brand_id          = request.args.get('brand', type=int)
   model_id          = request.args.get('model', type=int)
   seller_type       = request.args.get('seller_type')


   try:
      list_ad_infor = Ad.display(main_category_id=main_category_id, \
                                 region_id=region_id, area_id=area_id, \
                                 min_price=min_price, max_price=max_price, \
                                 brand_id=brand_id, model_id=model_id, \
                                 seller_type=seller_type, \
                                 page=page, category_id=category_id)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, list_ad_infor=list_ad_infor)


@ads.route('/subscribe', methods=['POST'])
@jwt_required
def subscribe():
   user_id     = get_jwt_identity()
   try:
      Subscription.init_from_request(user_id, request.json)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, message='Successfully subscribed')


@log.route('/create', methods=['POST'])
def create_log():
   try:
      AdEvent.init_from_request(request.json)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, message='Successfully logged')
