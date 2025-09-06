import pytz
from tzlocal import get_localzone

from datetime import datetime, tzinfo

# now = datetime.now()
# local_now = now.astimezone()
# local_tz = local_now.tzinfo

# print(local_tz)

# all_tznames = pytz.all_timezones
# for tz_name in all_tznames:
#     print(tz_name)

# print(datetime.now().tzinfo)
# print("Timezone:", datetime.now().tzname())

# print(datetime.now().astimezone().tzname())

print(get_localzone())


