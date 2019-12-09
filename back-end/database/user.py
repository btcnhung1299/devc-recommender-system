from datetime import datetime, date

from sqlalchemy import exists
from werkzeug.security import safe_str_cmp

import processing
from .db_model import db
from .utils import save_to_db
from recommend_main_category import recommend_main_category


class User(db.Model):
   __tablename__  = 'user'
   user_id        = db.Column(db.Integer, primary_key=True)
   phone          = db.Column(db.String(20), unique=True, nullable=False)
   register_date  = db.Column(db.Date, nullable=False,
                              default=datetime.utcnow().date)
   avatar         = db.Column(db.Text)
   name           = db.Column(db.String(150), nullable=False, default='user')
   gender         = db.Column(db.Enum('male', 'female', 'other'), default='other')
   birth_date     = db.Column(db.Date, default=date(2000, 1, 1))
   password       = db.Column(db.String(150), nullable=False)
   email          = db.Column(db.String(150), unique=True)
   region_id      = db.Column(db.Integer)
   area_id        = db.Column(db.Integer)

   def __init__(self, phone, password):
      self.phone     = phone
      self.password  = password 

   @staticmethod
   def get_recommended_main_category(user_fp):
      return recommend_main_category(user_fp)

   def get_basic_profile(self):
      area_name, region_name = processing.annot_loc(self.area_id, self.region_id)
      profile = { 'phone': self.phone, 'name': self.name, 'avatar': self.avatar,
                  'region': region_name, 'area': area_name }
      return profile
      
   def get_profile(self):
      """Get full user profile which extend from summary profile
      with user's birthdate and gender
      """
      birth_date = { 'day': self.birth_date.day, 'month': self.birth_date.month,
                     'year': self.birth_date.year}
      profile = self.get_basic_profile()
      profile['birth_date'] = birth_date
      profile['gender'] = self.gender
      return profile

   def update_from_request(self, args):
      """Update user profile by parsing request arguments
      and commit changes to database

      Raises:
         KeyError: Wrong format of date
         AttributeError: Named attribute does not exist
      """
      attrs = ['avatar', 'name', 'gender', 'email', 'region_id', 'area_id', 'birth_date']
      for attr in attrs:
         val = args.get(attr)
         if val is None:
            continue        
         if attr == 'birth_date':
            val = processing.date_from_str(val)
         setattr(self, attr, val)
      save_to_db(self)

   @staticmethod
   def init_from_request(args):
      """Create a new user by parsing request arguments
      and insert into database

      Raises:
         KeyError: Can't found required arguments in requests
         ConstraintViolation: Can't insert a new record due to Constraint Violation 
         IntegrityError: Can't insert a new record due to IntegrityError
         PhoneRegistered: Phone provided is already taken by another account
         PhoneWrongFormat: Phone provided is not properly formatted
         UnicodeError: Can't encode password for storing
      """
      phone = args['phone']

      if not processing.is_valid_phone(phone):
         raise Exception('PhoneWrongFormat')
         return

      if db.session.query(exists().where(User.phone == phone)).scalar():
         raise Exception('PhoneRegistered')
         return

      password = processing.hash_password(args['password'])
      new_user = User(phone=phone, password=password)
      save_to_db(new_user)

   @staticmethod
   def authenticate(phone, password):
      """Verify log-in by checking phone and password

      Return:
         (user's ID, username) if there is an account associated with provided
      phone and password

      Raise:
         PhoneUnrecognized: Phone provided is not associated with any account
         Unauthorized: Fail to authorize with provided information
         AttributeError: Referenced attributes can't be found in table
      """
      if not db.session.query(exists().where(User.phone == phone)).scalar():
         raise Exception('PhoneUnrecognized')
         return

      user = db.session.query(User.user_id, User.password, User.name) \
             .filter(User.phone == phone).one()      
      db_password = user.password
      password = processing.hash_password(password)

      if not safe_str_cmp(password, db_password):
         raise Exception('Unauthorized')
         return
   
      return (user.user_id, user.name)
