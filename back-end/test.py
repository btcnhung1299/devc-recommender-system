import datetime
my_str = '2019-09-12 11:08:37.000'
dt = datetime.datetime.strptime(my_str, '%Y-%m-%d %H:%M:%S.%)
print(dt)
