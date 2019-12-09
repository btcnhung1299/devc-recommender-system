import json

import processing


with open('encoding_tbl/stats_by_session.json', 'r') as json_file:
   last_stats = json.load(json_file)

stats = dict()
# `user_A` = {'stats': {'1.0': {'CLICK': [1, 2, 0, 0, 1], 'LOAD: [20, 10, 0, 5, 5]},
#                       '2.0': ...,
#                       '13.0': ...}
#             'last_activity': '12/12/2019 00:00'}
# `user_B` = {...}

for user, val in last_stats.items():
      stats[user] = dict()
      stats[user]['by_category'] = processing.stats_by_category(val)
      stats[user]['last_activity'] = processing.datetime_from_str(val['last_activity'])
      print(stats[user])
      break

def recommend_main_category(user, dt):
   pass 

def update_stats_main_category(user, event_type, dt):
   pass

