#!/usr/bin/python
import dateutil.parser
import pytz

in_date_str = input("Give your ist time:")
in_date = dateutil.parser.parse(in_date_str)
ist_date = pytz.timezone('Asia/Kolkata').localize(in_date)
utc_date = ist_date.astimezone(pytz.UTC)

print (f"epoch: {utc_date.timestamp()}")
print (f"{utc_date.isoformat()}")

