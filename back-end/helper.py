from flask_babel import Babel, format_timedelta, format_currency
import hashlib, re, unicodedata
import json
from datetime import datetime, date, timedelta

babel = Babel(default_locale='vi')

with open('encoding_tbl/config_location.json', encoding='utf8') as json_file:
   location_cs    = json.load(json_file)

with open('encoding_tbl/config_category.json', encoding='utf8') as json_file:
   category_cs    = json.load(json_file)

with open('encoding_tbl/config_ad.json', encoding='utf8') as json_file:
   adparam_cs     = json.load(json_file)


def normalize_location(area_id, region_id):
   if area_id is None or region_id is None:
      return (None, None)

   loc_id            = region_id // 1000
   loc, region, area = map(str, (loc_id, region_id, area_id))
   region_name       = location_cs[loc][region]['region_name']
   area_name         = location_cs[loc][region]['area'][area]
   return (area_name, region_name)


def normalize_category(category_id, main_category_id):
   if category_id is None or main_category_id is None:
      return (None, None)

   category, main_category = map(str, (category_id, main_category_id))
   main_category_name      = category_cs[main_category]['main_category_name']
   category_name           = category_cs[main_category]['category'][category]
   return (category_name, main_category_name)


def normalize_param(category_id, name, value):
   category          = str(category_id)
   try:
      param_val      = adparam_cs[category][name][value]
   except:
      try:
         param_val   = adparam_cs['0'][name][value]
      except:
         param_val   = value

   return param_val


def price_to_str(price):
   return format_currency(number=price, currency='VND')

def duration_to_str(previous_date):
   time_delta  = datetime.utcnow() - previous_date
   delta_str   = format_timedelta(time_delta)
   return '{} trước'.format(delta_str)


def date_from_str(date):
   try:
      day, month, year = date['day'], date['month'], date['year']
   except KeyError:
      raise Exception('Wrong date format')
      return 

   ddmmyy_str  = '{}/{}/{} 00:00'.format(day, month, year)
   return datetime.strptime(ddmmyy_str, '%d/%m/%Y %H:%M').date()


salt = 'Cahopteam9812-D15v6C'
def hash_password(password):
   password = (password + salt).encode()
   return hashlib.md5(password).hexdigest()


def parse_or_pass(obj, name, request):
   try:
      setattr(obj, name, request[name])
   except KeyError:
      pass
