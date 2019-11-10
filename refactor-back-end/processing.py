import hashlib
import re

def hash_password(password):
   salt        = 'Cahopteam9812-D15v6C'
   password    = (password + salt).encode()
   return hashlib.md5(password).hexdigest()

def is_valid_phone(phone):
   return all(each.isdigit() or each in ['+', '(', ')'] for each in phone)
