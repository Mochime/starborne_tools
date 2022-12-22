import datetime
import math

# Inputs
distance = 4

speed = 20


tt_hrs = distance/speed

hrs = math.floor(tt_hrs)
mins = math.floor((tt_hrs - hrs)*60)
secs = ((tt_hrs - hrs)*60 - mins)*60

print('Travel time:\n {} hours, {} mins, {} secs\n'.format(hrs,mins,secs))


# To calculate the return time of a 2-way movement, enter the landing time of the first leg below
# Only the hour, minute, second fields really matter
leave_time = datetime.datetime(2022,4,18, 21, 8, 0)  # Yr,Mon,Day, Hr, Min, Sec

schedule_time = leave_time + datetime.timedelta(hours=tt_hrs)
print('Scheduled return time:\n',schedule_time)

