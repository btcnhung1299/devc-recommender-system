"""
Create a sqlalchemy object (without app binding)
Load tables and helper functions
"""
from flask_sqlalchemy import SQLAlchemy
db       = SQLAlchemy()
#from user import User

"""
# Import model for classification
with open('model/model.pkl', 'rb') as model:
   classify_click = pickle.load(model)

with open('encoding_tbl/config_ctr.json') as json_file:
   ctr_dict = json.load(json_file)

with open('encoding_tbl/config_price_vs_avg.json') as json_file:
   price_vs_avg_dict = json.load(json_file)
"""


