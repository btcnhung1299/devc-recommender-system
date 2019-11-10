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
