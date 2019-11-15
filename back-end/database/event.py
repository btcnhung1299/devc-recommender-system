from datetime import datetime

from .db_model import db
from .utils import save_to_db


class Event(db.Model):
   __tablename__        = 'event'
   event_id             = db.Column(db.Integer, primary_key=True)
   adlist_id            = db.Column(db.Integer, nullable=False)
   ad_placement         = db.Column(db.Enum('top', 'default', 'bottom'), default='default')
   ad_position          = db.Column(db.Integer)
   ad_source            = db.Column(db.Enum('classifyad', 'stickyad', 'similarad'), default='classifyad')
   user_fingerprint     = db.Column(db.Text)
   event_client_time    = db.Column(db.DateTime)
   event_server_time    = db.Column(db.DateTime, default=datetime.utcnow)
   page_name            = db.Column(db.Enum('ADLISTING', 'ADVIEW'))
   page_number          = db.Column(db.Integer)
   page_device          = db.Column(db.Enum('DESKTOP', 'MOBILE'))
   filter_brand_id            = db.Column(db.Integer)
   filter_main_category_id    = db.Column(db.Integer)
   filter_category_id         = db.Column(db.Integer)
   filter_keyword             = db.Column(db.Text)
   filter_price               = db.Column(db.String(100))
   filter_region_id           = db.Column(db.Integer)
   filter_area_id             = db.Column(db.Integer)
   filter_adtype              = db.Column(db.Enum('all', 'let', 'rent', 'sell', 'buy'), default='all')

   def __init__(self, adlist_id, ad_placement, ad_position, ad_source,
                page_name, page_number, page_device,
                user_fingerprint, event_client_time, event_server_time,
                filter_brand_id, filter_main_category_id, filter_category_id, 
                filter_price, filter_keyword, filter_adtype, 
                filter_region_id, filter_area_id):
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
      self.filter_brand_id          = filter_brand_id
      self.filter_main_category_id  = filter_main_category_id
      self.filter_category_id       = filter_category_id
      self.filter_keyword           = filter_keyword
      self.filter_price             = filter_price
      self.filter_region_id         = filter_region_id
      self.filter_area_id           = filter_area_id
      self.filter_adtype            = filter_adtype


   @staticmethod
   def init_from_request(args):
      adlist_id            = args['adlist_id']
      ad_placement         = args['ad_placement']
      ad_position          = args['ad_position']
      ad_source            = args['ad_source']
      user_fingerprint     = args['user_fingerprint']
      event_client_time    = args['event_client_time']
      event_server_time    = args['event_server_time']
      page_name            = args['page_name']
      page_number          = args['page_number']
      page_device          = args['page_device']
      filter_brand_id      = args['filter_brand_id']
      filter_main_category_id    = args['filter_main_category_id']
      filter_category_id         = args['filter_category_id']
      filter_keyword             = args['filter_keyword']
      filter_price               = args['filter_price']  
      filter_region_id           = args['filter_region_id']
      filter_area_id             = args['filter_area_id']
      filter_adtype              = args['filter_adtype']

      new_ad_event = Event(adlist_id=adlist_id, ad_placement=ad_placement, ad_position=ad_position, ad_source=ad_source,
                           user_fingerprint=user_fingerprint, page_device=page_device, page_number=page_number, page_name=page_name,
                           event_client_time=event_client_time, event_server_time=event_server_time,
                           filter_brand_id=filter_brand_id, filter_main_category_id=filter_main_category_id,
                           filter_category_id=filter_category_id, filter_adtype=filter_adtype,
                           filter_keyword=filter_keyword, filter_price=filter_price,
                           filter_region_id=filter_region_id, filter_area_id=filter_area_id)
      save_to_db(new_ad_event)
