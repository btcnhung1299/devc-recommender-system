import hashlib
import re
import json
from datetime import datetime

from flask_babel import Babel, format_timedelta, format_currency

babel = Babel(default_locale='vi')

def hash_password(password):
   salt        = 'Cahopteam9812-D15v6C'
   password    = (password + salt).encode()
   return hashlib.md5(password).hexdigest()


def is_valid_phone(phone):
   return all(each.isdigit() or each in ['+', '(', ')'] for each in phone)


def date_from_str(date):
   day, month, year  = date['day'], date['month'], date['year']
   ddmmyy_str        = '{}/{}/{} 00:00'.format(day, month, year)
   return datetime.strptime(ddmmyy_str, '%d/%m/%Y %H:%M').date()


def price_to_str(price):
   return format_currency(number=price, currency='VND')


def duration_to_str(previous_date):
   time_delta  = datetime.utcnow() - previous_date
   delta_str   = format_timedelta(time_delta)
   return '{} trước'.format(delta_str)


with open('encoding_tbl/config_location.json', encoding='utf8') as json_file:
   location_cs       = json.load(json_file)

def annot_loc(area_id, region_id):
   if area_id is None or region_id is None:
      return (None, None)

   loc_id            = region_id // 1000
   loc, region, area = map(str, (loc_id, region_id, area_id))
   region_name       = location_cs[loc][region]['region_name']
   area_name         = location_cs[loc][region]['area'][area]
   return (area_name, region_name)


with open('encoding_tbl/config_category.json', encoding='utf8') as json_file:
   category_cs    = json.load(json_file)

def annot_cat(category_id, main_category_id):
   if category_id is None or main_category_id is None:
      return (None, None)

   category, main_category = map(str, (category_id, main_category_id))
   main_category_name      = category_cs[main_category]['main_category_name']
   category_name           = category_cs[main_category]['category'][category]
   return (category_name, main_category_name)
