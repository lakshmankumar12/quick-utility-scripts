#!/usr/bin/python
import dateutil.parser
import pytz
import os
from dataclasses import dataclass

@dataclass
class TzInfo:
    unix: str
    colloquial : str
    abbr: str
    abbr_d: str       ## daylight savings abbr

interested_zones = [
    TzInfo('Etc/UTC',                     'UTC',      'UTC',   ''),
    TzInfo('Asia/Kolkata',                'IST',      'IST',   ''),
    TzInfo('America/New_York',            'Eastern',  'EST',   'EDT'),
    TzInfo('America/North_Dakota/Center', 'Central',  'CST',   'CDT'),
    TzInfo('America/Denver',              'Mountain', 'MST',   'MDT'),
    TzInfo('America/Los_Angeles',         'Pacific',  'PST',   'PDT'),
    TzInfo('America/Anchorage',           'Alaska',   'AKST',  'AKDT'),
    TzInfo('America/Phoenix',             'Arizona',  'MST',   'MST'),
    TzInfo('Pacific/Honolulu',            'Hawaii',   'HST',   'HDT'),
]

def build_tables():
    by_unix = {}
    by_colloquial = {}
    by_abbr = {}
    for i in interested_zones:
        by_unix[i.unix] = i
        by_colloquial[i.colloquial] = i
        if i.abbr and i.abbr not in by_abbr:
            by_abbr[i.abbr] = i
        if i.abbr_d and i.abbr_d not in by_abbr:
            by_abbr[i.abbr_d] = i
    return by_unix, by_colloquial, by_abbr

def get_inzone(by_unix, by_coll, by_abbr):
    info = None
    tabbr = os.getenv('TABBR', "")
    if tabbr:
        info = by_abbr.get(tabbr, None)
    if info is not None:
        return info
    tcoll = os.getenv('TCOLL', "")
    if tcoll:
        info = by_coll.get(tcoll, None)
    if info is not None:
        return info
    unixzone = os.getenv('TZ', 'Asia/Kolkata')
    info = by_unix[unixzone]
    return info

def ask_and_compute(inzone):
    print (f"Influential env-vars in order: TABBR:{os.getenv('TABBR','unset')}, TCOLL:{os.getenv('TCOLL','unset')}, TZ:{os.getenv('TZ','unset')}")
    in_date_str = input(f"Give your {inzone.colloquial} time: ")
    in_date = dateutil.parser.parse(in_date_str)
    inzone_date = pytz.timezone(inzone.unix).localize(in_date)
    utc_date = inzone_date.astimezone(pytz.UTC)
    return utc_date

def print_all(date):
    print (f"epoch: {date.timestamp()}")
    for z in interested_zones:
        zonetime = date.astimezone(pytz.timezone(z.unix))
        print (f"Time in zone: {z.unix:30s} {z.colloquial:10s} is  {zonetime.isoformat()} {zonetime.strftime('%Z')}")

u,c,a = build_tables()
info = get_inzone(u,c,a)
d = ask_and_compute(info)
print_all(d)
