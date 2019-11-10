from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_method

import database.views as views
import processing
from .db_model import db
from .utils import save_to_db

class Ad(db.Model):
   __tablename__     = 'ad'
   adlist_id         = db.Column(db.Integer, primary_key=True)
   owner_id          = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
   create_at         = db.Column(db.DateTime, default=datetime.utcnow)
   is_sticky         = db.Column(db.Boolean, default=False)
   seller_type       = db.Column(db.Enum('pro', 'private'), default='private')
   adtype            = db.Column(db.Enum('let', 'rent', 'sell', 'buy'))
   main_category_id  = db.Column(db.Integer, nullable=False)
   category_id       = db.Column(db.Integer, nullable=False)
   subject           = db.Column(db.String(500), nullable=False)
   price             = db.Column(db.Integer, nullable=False)
   content           = db.Column(db.Text, nullable=False)
   number_of_img     = db.Column(db.Integer, default=0)
   image_url         = db.Column(db.Text)
   thumbnail_img_url = db.Column(db.Text)
   region_id         = db.Column(db.Integer)
   area_id           = db.Column(db.Integer)

   def __init__(self, owner_id, main_category_id, category_id, adtype, seller_type, subject, price, content, number_of_img, \
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
   
   def get_summary(self):
      user                    = views.User.query.get(self.owner_id)
      area_name, region_name  = processing.annot_loc(self.area_id, self.region_id)
      price_str               = processing.price_to_str(self.price)
      create_at_str           = processing.duration_to_str(self.create_at)
      category_name, main_category_name = processing.annot_cat(self.category_id, self.main_category_id)   

      summary = {'subject': self.subject, 'price_str': price_str, 'region': region_name, 'area': area_name, \
                 'is_sticky': self.is_sticky, 'seller_type': self.seller_type, 'category_name': category_name, \
                 'main_category_name': main_category_name, 'number_of_img': self.number_of_img, 'create_elapse': create_at_str, \
                 'thumbnail_img_url': self.thumbnail_img_url, 'adlist_id': self.adlist_id}
 
      summary['publisher']       = user.get_basic_profile()
      summary['publisher']['id'] = self.owner_id
      return summary
 
   def get_infor(self):
      infor                = self.get_summary()
      infor['date']        = self.create_at
      infor['content']     = self.content
#      infor['parameters']  = views.AdParam.get_infor(self.adlist_id, self.category_id)
      return infor

   @hybrid_method
   def belongs(self, main_category_id, category_id, min_price, max_price):
      return False

   @belongs.expression
   def belongs(cls, main_category_id, category_id, min_price, max_price, seller_type, region_id, area_id):
      cmp_res     = (main_category_id == None or cls.main_category_id == main_category_id)
      cmp_res     &= (category_id == None or cls.category_id == category_id)
      cmp_res     &= (region_id == None or cls.region_id == region_id)
      cmp_res     &= (area_id == None or cls.area_id == area_id)
      cmp_res     &= (min_price == None or cls.price >= min_price)
      cmp_res     &= (max_price == None or cls.price <= max_price)
      cmp_res     &= (seller_type == None or cls.seller_type == seller_type)
      return cmp_res



   @staticmethod
   def init_from_request(owner_id, args):
      basics, params       = args['basics'], args['parameters']
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
      new_ad = Ad(owner_id=owner_id, seller_type=seller_type, main_category_id=main_category_id, price=price, \
                  category_id=category_id, subject=subject, content=content, number_of_img=number_of_img, \
                  image_url=image_url, region_id=region_id, area_id=area_id, adtype=adtype, thumbnail_img_url=thumbnail_img_url)

      save_to_db(new_ad)
      #AdParam.init_from_request(adlist_id=new_ad.adlist_id, request=params)
   
   @staticmethod
   def display(main_category_id, category_id, page, min_price, max_price, brand_id, model_id, seller_type, region_id, area_id):
      if page     == None:
         page     = 0

      s_ad_pos    = page * page_size
      e_ad_pos    = s_ad_pos + page_size
      try:
         ad_list  = db.session.query(Ad).order_by(desc(Ad.adlist_id)).filter(Ad.belongs(main_category_id=main_category_id, \
                                    category_id=category_id, min_price=min_price, max_price=max_price, seller_type=seller_type, \
                                    region_id=region_id, area_id=area_id)).slice(s_ad_pos, e_ad_pos)
      except Exception as error:
         raise Exception('QueryFail: {}', str(error))
         return

      infor       = [ad.get_summary() for ad in ad_list]
      return infor

"""
   def get_avg_price(self):
      try:
         p = price_vs_avg_dict[str(self.adlist_id)]
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
"""
