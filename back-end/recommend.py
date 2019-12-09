import json

import processing


with open('encoding_tbl/stats_by_session.json', 'r') as json_file:
   last_stats = json.load(json_file)

stats = dict()
# `user_A` = {'by_category': {1:    {'CLICK': [1, 2, 0, 0, 1], 'LOAD': [20, 10, 0, 5, 5]},
#                             2:    {...}, ...
#                             13:   {...} },
#             'total': {'CLICK': [5, 7, 10, 11, 0], 'LOAD': [200, 10, 20, 20, 10]},
#             'last_activity': '12/12/2019 00:00'}
# `user_B` = {...}

user_fp = ''
for user, val in last_stats.items():
      stats[user] = dict()
      stats[user]['by_category'], stats[user]['total'] = processing.stats_by_category(val)
      stats[user]['last_activity'] = processing.datetime_from_str(val['last_activity'])
      user_fp = user
      break

def interest_by_category(user, cat):
   num_periods = len(stats[user]['total']['CLICK'])
   numerator = denominator = 0

   for t in range(num_periods):
      total_click_t = stats[user]['total']['CLICK'][t]
      total_load_t = stats[user]['total']['LOAD'][t]
            
      interest_t = stats[user]['by_category'][cat]['CLICK'][t] * stats[user]['by_category'][cat]['LOAD'][t]
      interest_t *= total_click_t
      interest_t /= total_load_t

      numerator += interest_t
      denominator += total_click_t

   return numerator / denominator 

def recommend_main_category(user):
   interests = [(interest_by_category(user, cat), cat) for cat in range(1, 13 + 1)]
   interests.sort(reverse=True)
   return [cat for interest, cat in interests]


def update_stats_main_category(user, event_type, dt):
   pass

