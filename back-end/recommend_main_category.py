import json
import datetime

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

NUM_CATEGORY = 13
MAX_NUM_SESSION = 5
SESSION_DURATION = datetime.timedelta(minutes=30)

for user, val in last_stats.items():
      stats[user] = dict()
      stats[user]['by_category'], stats[user]['total'] = processing.stats_by_category(val)
      stats[user]['last_activity'] = processing.datetime_from_str(val['last_activity'])



def create_new_history(user):
   stats[user] = dict()
   stats[user]['last_activity'] = datetime.datetime(year=2000, month=1, day=1)
   stats[user]['total'] = { 'CLICK': [0], 'LOAD': [0] }
   stats[user]['by_category'] = dict()
   for cat in range(1, NUM_CATEGORY + 1):
      stats[user]['by_category'][cat] = { 'CLICK': [0], 'LOAD': [0] }
  

def remove_oldest_session(user):
   for event in stats[user]['total'].keys():
      stats[user]['total'][event].pop(0)
      stats[user]['total'][event].append(0)

   for cat, event_stats in stats[user]['by_category'].items():
      for event in event_stats.keys():
         stats[user]['by_category'][cat][event].pop(0)
         stats[user]['by_category'][cat][event].append(0)    


def update_lastest_session(user, event, cat, dt):
   stats[user]['total'][event][-1] += 1
   stats[user]['by_category'][cat][event][-1] += 1
   stats[user]['last_activity'] = dt


def update_stats_main_category(user, event_type, cat, event_time_str):
   dt = processing.datetime_from_str(event_time_str)
   if user not in stats:
      create_new_history(user)

   new_session = (dt - stats[user]['last_activity']) > SESSION_DURATION
   if new_session:
      remove_oldest_session(user)
   update_lastest_session(user, event_type, cat, dt)


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
   interests = [(interest_by_category(user, cat), cat) for cat in range(1, NUM_CATEGORY + 1)]
   interests.sort(reverse=True)
   return [cat for interest, cat in interests]
