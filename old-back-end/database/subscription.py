from database import db

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


