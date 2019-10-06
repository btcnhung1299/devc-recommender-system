# Import flask extensions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, desc
from sqlalchemy.ext.hybrid import hybrid_method
from helper import normalize_location, normalize_category, normalize_param, price_to_str, duration_to_str, parse_or_pass, date_from_str, hash_password

# Import python standard libraries
from datetime import datetime, date
import json

# Import libaries for modeling
import pickle
import pandas as pd
from random import randint

# Create an instance of SQLAlchemy
db = SQLAlchemy()

# Global variables
page_size = 20

# Import model for classification
with open('model/model.pkl', 'rb') as model:
   classify_click = pickle.load(model)

with open('encoding_tbl/config_ctr.json') as json_file:
   ctr_dict = json.load(json_file)

with open('encoding_tbl/config_price_vs_avg.json') as json_file:
   price_vs_avg_dict = json.load(json_file)

# --------------------- HELPER FUNCTIONS -----------------
def save_to_db(model):
   try:
      db.session.add(model)
      db.session.commit()
   except exc.DataError:
      raise Exception('ConstraintViolation')
      return
   except exc.IntegrityError:
      raise Exception('IntegrityError')
      return
   except exc.SQLAlchemyError as error:
      raise Exception(str(error))
      return

# --------------------------- USER --------------------------
class User(db.Model):
   __tablename__ = 'user'
   
   # Attributes:
   user_id        = db.Column(db.Integer, primary_key=True)
   phone          = db.Column(db.String(20), unique=True, nullable=False)
   register_date  = db.Column(db.Date, nullable=False, \
                              default=datetime.utcnow().date)
   avatar         = db.Column(db.Text)
   name           = db.Column(db.String(150), nullable=False, \
                              default='user')
   gender         = db.Column(db.Enum('male', 'female', 'other'), \
                              default='other')
   birth_date     = db.Column(db.Date, default=date(2000, 1, 1))
   password       = db.Column(db.String(150), nullable=False)
   email          = db.Column(db.String(150), unique=True)
   region_id      = db.Column(db.Integer)
   area_id        = db.Column(db.Integer)

   # Constructor:
   def __init__(self, phone, password):
      self.phone     = phone
      self.password  = password
   
   # Create and save new user from request
   @staticmethod
   def init_from_request(response):
      try:
         phone       = response['phone']
         password    = hash_password(response['password'])
      except KeyError:
         raise Exception('Bad request format')
         return
      except UnicodeDecodeError:
         raise Exception('Cannot decode unicode string')
         return

      new_user = User(phone=phone, password=password)
      save_to_db(new_user)

   # Update user profile
   def update_from_request(self, request):
      possible_attr = ['avatar', 'name', 'gender', 'email', \
                       'region_id', 'area_id']
      for attr in possible_attr:
         parse_or_pass(self, attr, request)
     
      try:
         self.birth_date = date_from_str(request['birth_date'])
      except KeyError:      
         pass

      save_to_db(self)

   # Get basic info
   def get_basic_profile(self):
      area_name, region_name = \
            normalize_location(self.area_id, self.region_id)
      profile = {'phone': self.phone, 'name': self.name, \
                 'avatar': self.avatar, 'region': region_name, \
                 'area': area_name}
      return profile
      
   # Get user profile
   def get_profile(self):
      profile = self.get_basic_profile()
      birth_date = {'day': self.birth_date.day, \
                    'month': self.birth_date.month, \
                    'year': self.birth_date.year}
      profile['birth_date'] = birth_date
      profile['gender'] = self.gender
      return profile

'''
# --------------------- SUBSCRIPTION -------------------
class Subscription(db.Model):
   __tablename__     = 'subscription'

   # Attributes:
   user_id           = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
   ads_id            = db.Column(db.Integer, db.ForeignKey('ads.ads_id'), primary_key=True)

   def __init__(self, user_id, ads_id):
      self.user_id   = user_id
      self.ads_id    = ads_id

   @staticmethod
   def init_from_request(user_id, request):
      try:
         ads_id      = request['ads_id']
      except KeyError:
         raise Exception('Bad request format')
         return
      except UnicodeDecodeError:
         raise Exception('Cannot decode unicode string')
         return
      
      new_subscription  = Subscription(user_id, ads_id)
      save_to_db(new_subscription)
'''

# ------------------------- AD --------------------------
class Ad(db.Model):
   __tablename__     = 'ad'
   
   # Attributes:
   adlist_id         = db.Column(db.Integer, primary_key=True)
   owner_id          = db.Column(db.Integer, \
                                 db.ForeignKey('user.user_id'), \
                                 nullable=False)
   create_at         = db.Column(db.DateTime, default=datetime.utcnow)
   is_sticky         = db.Column(db.Boolean, default=False)
   seller_type       = db.Column(db.Enum('pro', 'private'), \
                                 default='private')
   adtype            = db.Column(db.Enum('let', 'rent', 'sell', 'buy'))
   main_category_id  = db.Column(db.Integer, nullable=False)
   category_id       = db.Column(db.Integer, nullable=False)
   subject           = db.Column(db.Text, nullable=False)
   price             = db.Column(db.Integer, nullable=False)
   content           = db.Column(db.Text, nullable=False)
   number_of_img     = db.Column(db.Integer, default=0)
   image_url         = db.Column(db.Text)
   thumbnail_img_url = db.Column(db.Text)
   region_id         = db.Column(db.Integer)
   area_id           = db.Column(db.Integer)
   
   # Constructor:
   def __init__(self, owner_id, main_category_id, category_id, adtype, \
                seller_type, subject, price, content, number_of_img, \
                image_url, thumbnail_img_url, region_id, area_id):
      self.owner_id           = owner_id
      self.main_category_id   = main_category_id
      self.category_id        = category_id
      self.seller_type        = seller_type
      self.adtype             = adtype
      self.subject            = subject
      self.price              = price
      self.content            = content
      self.number_of_img      = number_of_img
      self.image_url          = image_url
      self.thumbnail_img_url  = thumbnail_img_url
      self.region_id          = region_id
      self.area_id            = area_id

   # Create and save new item from request into database
   @staticmethod
   def init_from_request(owner_id, request):
      try:
         basics, params       = request['basics'], request['parameters']
         main_category_id     = basics['main_category_id']
         category_id          = basics['category_id']
         adtype               = basics['adtype']
         seller_type          = basics['seller_type']
         subject              = basics['subject']
         price                = basics['price']
         content              = basics['content']
         number_of_img        = basics['number_of_img']
         image_url            = basics['image_url']
         thumbnail_img_url    = basics['thumbnail_img_url']
         region_id            = basics['region_id']
         area_id              = basics['area_id']
      except KeyError:
         raise Exception('Bad request format')
         return
            
      new_ad = Ad(owner_id=owner_id, seller_type=seller_type, \
                  main_category_id=main_category_id, price=price, \
                  category_id=category_id, subject=subject, \
                  content=content, number_of_img=number_of_img, \
                  image_url=image_url, region_id=region_id, \
                  area_id=area_id, adtype=adtype, \
                  thumbnail_img_url=thumbnail_img_url)

      save_to_db(new_ad)
      AdParam.init_from_request(adlist_id=new_ad.adlist_id, \
                                request=params)
   
   def get_summary(self):
      user = User.query.get(self.owner_id)
      area_name, region_name = \
            normalize_location(self.area_id, self.region_id)
      category_name, main_category_name = \
            normalize_category(self.category_id, self.main_category_id)   
      price_str      = price_to_str(self.price)
      create_at_str  = duration_to_str(self.create_at)

      summary = {'subject': self.subject, 'price_str': price_str, \
                 'region': region_name, 'area': area_name, \
                 'is_sticky': self.is_sticky, 'seller_type': self.seller_type, \
                 'category_name': category_name, 'adlist_id': self.adlist_id, \
                 'main_category_name': main_category_name, \
                 'number_of_img': self.number_of_img, 'create_elapse': create_at_str, \
                 'thumbnail_img_url': self.thumbnail_img_url}
 
      summary['publisher'] = user.get_basic_profile()
      summary['publisher']['id'] = self.owner_id
      return summary
 
   # Get ads infor
   def get_infor(self):
      infor                = self.get_summary()
      infor['date']        = self.create_at
      infor['content']     = self.content
      infor['parameters']  = AdParam.get_infor(self.adlist_id, self.category_id)
      return infor

   # Filter ads
   @hybrid_method
   def belongs(self, main_category_id, category_id, min_price, max_price):
      return False

   @belongs.expression
   def belongs(cls, main_category_id, category_id, min_price, max_price, \
               seller_type, region_id, area_id):
      cmp_res     = (main_category_id == None or \
                     cls.main_category_id == main_category_id)
      cmp_res     &= (category_id == None or cls.category_id == category_id)
      cmp_res     &= (region_id == None or cls.region_id == region_id)
      cmp_res     &= (area_id == None or cls.area_id == area_id)
      cmp_res     &= (min_price == None or cls.price >= min_price)
      cmp_res     &= (max_price == None or cls.price <= max_price)
      cmp_res     &= (seller_type == None or cls.seller_type == seller_type)
      return cmp_res
   
   # Display ads with filters (if exist)
   @staticmethod
   def display(main_category_id, category_id, page, min_price, \
               max_price, brand_id, model_id, seller_type, \
               region_id, area_id):
      if page == None:
         page = 0

      s_ad_pos    = page * page_size
      e_ad_pos    = s_ad_pos + page_size
      try:
         ad_list  = db.session.query(Ad).order_by(desc(Ad.adlist_id)). \
                    filter(Ad.belongs(main_category_id=main_category_id, \
                           category_id=category_id, min_price=min_price, \
                           max_price=max_price, seller_type=seller_type, \
                           region_id=region_id, area_id=area_id)). \
                    slice(s_ad_pos, e_ad_pos)
      except Exception as error:
         raise Exception('Something happened during query process.', str(error))

         return

      infor = [ad.get_summary() for ad in ad_list]
      return infor

   def get_avg_price(self):
      try:
         p = price_vs_avg_dict[str(self.adlist_id)]
         print('yes')
      except:
         p = self.price
      return p      

   # Classify if the current ad will be clicked by a user
   def will_click(self, user_fingerprint):
      inp = dict()
      inp['category_id'] = self.category_id
      inp['region'] = self.region_id
      inp['price_vs_avg'] = self.price - self.get_avg_price()
      inp['seller_type'] = (0 if self.seller_type == 'private' else 1)
      inp['user_fingerprint'] = 24
      inp['content_length'] = len(self.content)
      inp['subject_length'] = len(self.subject)
      inp['price'] = self.price
      try:
         inp['crt'] = ctr_dict['click'][str(self.adlist_id)]
         print(inp['crt'])
      except:
         inp['crt'] = 0

      X = pd.Series(inp).to_frame().T
      X = X.reindex(sorted(X.columns), axis=1)
      return classify_click.predict(X)[0]      

   # Return list of recommended ads
   @staticmethod
   def general_recommend(user_fingerprint):
      limit_batch = 40
      recent_ads = db.session.query(Ad).order_by(desc(Ad.adlist_id)).limit(limit_batch)
      marked_ads = [0] * limit_batch
      n_ads = 0
      choose_ads = []

      # If there is less than 5 ads to be recommended, randomize them
      while len(choose_ads) < 5 and n_ads < limit_batch:
         i = randint(0, limit_batch)
         n_ads += 1
         if marked_ads[i] == 0:
            if recent_ads[i].will_click(user_fingerprint):
               choose_ads.append(recent_ads[i].get_summary())
               marked_ads[i] = 1
            else:
               marked_ads[i] = -1
           
      for i in range(limit_batch):
         if len(choose_ads) == 5:
            break
         if marked_ads[i] == -1:
            choose_ads.append(recent_ads[i].get_summary())

      return choose_ads[:5]


# ---------------------- AD-PARAM ------------------------
class AdParam(db.Model):
   __tablename__  = 'ad_param'

   # Attributes:
   adlist_id      = db.Column(db.Integer, \
                              db.ForeignKey('ad.adlist_id'), \
                              primary_key=True)
   name           = db.Column(db.String(100), primary_key=True)
   value          = db.Column(db.String(500))

   # Constructor:
   def __init__(self, adlist_id, name, value):
      self.adlist_id    = adlist_id
      self.name         = name
      self.value        = value

   @staticmethod
   def init_from_request(adlist_id, request):
      for attr, value in request.items():
         new_param = AdParam(adlist_id=adlist_id, name=attr, value=value)
         save_to_db(new_param)
         
   @staticmethod
   def get_infor(adlist_id, category_id):
      try:
         params = db.session.query(AdParam.name, AdParam.value). \
                  filter(AdParam.adlist_id == adlist_id)
      except AttributeError:
         raise Exception('AttributeError')
         return

      
      infor    = [{'name': each.name, 'value_id': each.value, \
                  'value': normalize_param(category_id, each.name, each.value)}
                  for each in params]
      return infor

# -------------------------- AdEvent -------------------------
class AdEvent(db.Model):
   __tablename__  = 'ad_event'

   # Attributes:
   adevent_id           = db.Column(db.Integer, primary_key=True)
   adlist_id            = db.Column(db.Integer, nullable=False)
   ad_placement         = db.Column(db.Enum('top', 'default', 'bottom'), \
                                    default='default')
   ad_position          = db.Column(db.Integer)
   ad_source            = db.Column(db.Enum('classifyad', 'stickyad', \
                                    'similarad'), default='classifyad')
   user_fingerprint     = db.Column(db.Text)
   event_client_time    = db.Column(db.DateTime)
   event_server_time    = db.Column(db.DateTime, default=datetime.utcnow)
   page_name            = db.Column(db.Enum('ADLISTING', 'ADVIEW'))
   page_number          = db.Column(db.Integer)
   page_device          = db.Column(db.Enum('DESKTOP', 'HANDY'))
   filter_brand         = db.Column(db.Integer)
   filter_main_category_id = db.Column(db.Integer)
   filter_category_id   = db.Column(db.Integer)
   filter_keyword       = db.Column(db.Text)
   filter_price         = db.Column(db.String(100))
   filter_region_id     = db.Column(db.Integer)
   filter_area_id       = db.Column(db.Integer)
   filter_adtype        = db.Column(db.Enum('all', 'let', 'rent', 'sell', \
                                    'buy'), default='all')

   # Constructor
   def __init__(self, adlist_id, ad_placement, ad_position, ad_source, \
                user_fingerprint, event_client_time, event_server_time, \
                page_name, page_number, page_device, filter_brand, \
                filter_main_category_id, filter_category_id, \
                filter_keyword, filter_price, filter_region_id, \
                filter_area_id, filter_adtype):
      self.adlist_id          = adlist_id
      self.ad_placement       = ad_placement
      self.ad_position        = ad_position
      self.ad_source          = ad_source
      self.user_fingerprint   = user_fingerprint
      self.event_client_time  = event_client_time
      self.event_server_time  = event_server_time
      self.page_name          = page_name
      self.page_number        = page_number
      self.page_device        = page_device
      self.filter_brand       = filter_brand
      self.filter_main_category_id  = filter_main_category_id
      self.filter_category_id       = filter_category_id
      self.filter_keyword     = filter_keyword
      self.filter_price       = filter_price
      self.filter_region_id   = filter_region_id
      self.filter_area_id     = filter_area_id
      self.filter_adtype      = filter_adtype


   # Create and save an event from request
   @staticmethod
   def init_from_request(request):
      try:
         adlist_id            = request['adlist_id']
         ad_placement         = request['ad_placement']
         ad_position          = request['ad_position']
         ad_source            = request['ad_source']
         user_fingerprint     = request['user_fingerprint']
         event_client_time    = request['event_client_time']
         event_server_time    = request['event_server_time']
         page_name            = request['page_name']
         page_number          = request['page_number']
         page_device          = request['page_device']
         filter_brand         = request['filter_brand']
         filter_main_category_id    = request['filter_main_category_id']
         filter_category_id         = request['filter_category_id']
         filter_keyword       = request['filter_keyword']
         filter_price         = request['filter_price']  
         filter_region_id     = request['filter_region_id']
         filter_area_id       = request['filter_area_id']
         filter_adtype        = request['filter_adtype']
      except:
         raise Exception('Bad request format')
         return

      new_ad_event = AdEvent(adlist_id=adlist_id, ad_placement=ad_placement, \
                             ad_position=ad_position, ad_source=ad_source, \
                             user_fingerprint=user_fingerprint, page_number=page_number, \
                             event_client_time=event_client_time, \
                             event_server_time=event_server_time, \
                             page_name=page_name, page_device=page_device, \
                             filter_brand=filter_brand, filter_price=filter_price, \
                             filter_main_category_id=filter_main_category_id, \
                             filter_category_id=filter_category_id, \
                             filter_keyword=filter_keyword, filter_adtype=filter_adtype, \
                             filter_region_id=filter_region_id, filter_area_id=filter_area_id)
      save_to_db(new_ad_event)

