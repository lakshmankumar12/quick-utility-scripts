#!/usr/bin/python
import dateutil.parser
import pytz
import os

tzone = os.getenv('TZ', 'Asia/Kolkata')

in_date_str = input(f"Give your {tzone} time:")
in_date = dateutil.parser.parse(in_date_str)
inzone_date = pytz.timezone(tzone).localize(in_date)
utc_date = inzone_date.astimezone(pytz.UTC)

interested_zones = [
        ['Etc/UTC',               'UTC'],
        ['Asia/Kolkata',         'IST'],
        ['America/New_York',      'Eastern'],
        ['America/North_Dakota/Center', 'Central'],
        ['America/Denver',        'Mountain'],
        ['America/Los_Angeles',   'Pacific'],
        #['America/Anchorage',       'Alaska'],
        #['America/Phoenix',         'Arizona'],
        #['America/Honolulu',        'Hawaii'],
]

print (f"epoch: {utc_date.timestamp()}")

for z,name in interested_zones:
    zonetime = utc_date.astimezone(pytz.timezone(z))
    print (f"Time in zone: {name:10s} is  {zonetime.isoformat()}")

