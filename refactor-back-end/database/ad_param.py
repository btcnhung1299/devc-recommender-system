import processing

from .db_model import db
from .utils import save_to_db


class AdParam(db.Model):
   __tablename__        = 'ad_param'
   adlist_id            = db.Column(db.Integer, db.ForeignKey('ad.adlist_id'), primary_key=True)
   name                 = db.Column(db.String(100), primary_key=True)
   value                = db.Column(db.String(500))

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
         params = db.session.query(AdParam.name, AdParam.value).filter(AdParam.adlist_id == adlist_id)
      except AttributeError as error:
         raise Exception(type(error).__name__)
         return
      except Exception as error:
         raise Exception(str(error))
         return
      
      infor = {each.name: {'value_id': each.value, 'value': processing.annot_param(category_id, each.name, each.value)}
               for each in params}
      return infor
