import argparse
from datetime import datetime
import requests
import time
from operator import sub
import os

ENPHASE_APP_KEY = os.environ['ENPHASE_APP_KEY']
ENPHASE_USER_ID = os.environ['ENPHASE_USER_ID']
ENPHASE_SYSTEM_ID = os.environ['ENPHASE_SYSTEM_ID']

AUTH_PARAMS = {
    'key': ENPHASE_APP_KEY,
    'user_id': ENPHASE_USER_ID
}
TIME_INTERVAL_PARAMS = lambda start, end: {
    'start_at': start,
    'end_at': end
}
ENPHASE_BASE_URL = 'https://api.enphaseenergy.com/api/v2'
STATS = lambda start, end, isForProduction: '{base}/systems/{sysId}/{endpoint}?{params}'.format(
    base=ENPHASE_BASE_URL,
    sysId=ENPHASE_SYSTEM_ID,
    endpoint='rgm_stats' if isForProduction else 'consumption_stats',
    params=getUrlParams(TIME_INTERVAL_PARAMS(start, end), AUTH_PARAMS)
)

OFF_PEAK_END_HR = 8
SUPER_OFF_PEAK_END_HR = 16
PEAK_END_HR = 21
WATTS_TO_KWH = .001
DECIMAL_PLACES = 1
FIRST_COL_WIDTH = 40

def getUrlParams(*args):
    '''Return a string consisting of url params of all k v pairs in the dicts in args'''
    mergedDict = {}
    for arg in args:
        mergedDict.update(arg)
    return '&'.join(['{}={}'.format(k, v) for k,v in mergedDict.items()])

def date(dateString):
    '''Convert date from mm/dd/yy format to a Unix timestamp'''
    return datetime.strptime(dateString, '%m/%d/%y').timestamp()

def printStats(cpn, offPeakKwh, superOffPeakKwh, peakKwh):
    '''Print stats for consumption, production, or net (cpn)'''
    print ('{:40}{} kwh'.format(
        'off peak {} (< {:02}:00)'.format(cpn, OFF_PEAK_END_HR),
        round(offPeakKwh, DECIMAL_PLACES)
    ))
    print ('{:40}{} kwh'.format(
        'super off {} (< {:02}:00)'.format(cpn, SUPER_OFF_PEAK_END_HR),
        round(superOffPeakKwh, DECIMAL_PLACES)
    ))
    print ('{:40}{} kwh'.format(
        'peak {} (< {:02}:00)'.format(cpn, PEAK_END_HR),
        round(peakKwh, DECIMAL_PLACES)
    ))
    print ()

def getStats(start, end, isForProduction, printThem=True):
    '''Call Enphase API to get consumption or production stats between given timestamps'''
    r = requests.get(url=STATS(start, end, isForProduction))
    intervals = r.json()['intervals']
    
    offPeakKwh = 0
    superOffPeakKwh = 0
    peakKwh = 0
    for interval in intervals:
        intervalEndTimestamp = interval['end_at'] - 1
        hr = int(datetime.fromtimestamp(intervalEndTimestamp).strftime('%H'))
        kwh = interval['wh_del' if isForProduction else 'enwh'] * WATTS_TO_KWH

        if hr < OFF_PEAK_END_HR:
            offPeakKwh += kwh
        elif hr < SUPER_OFF_PEAK_END_HR:
            superOffPeakKwh += kwh
        elif hr < PEAK_END_HR:
            peakKwh += kwh
        else:  # back to off peak
            offPeakKwh += kwh

    state = 'production' if isForProduction else 'consumption'
    printStats(state, offPeakKwh, superOffPeakKwh, peakKwh)

    return offPeakKwh, superOffPeakKwh, peakKwh

if __name__ == '__main__':
    # get start and end timestamps from console args
    parser = argparse.ArgumentParser(
        description='Get consumption report for the given time interval'
    )
    parser.add_argument('--start', required=True, help='Start date in mm/dd/yy format', type=date)
    parser.add_argument('--end', required=True, help='End date in mm/dd/yy format', type=date)
    args = parser.parse_args()
    start, end = args.start, args.end

    # get consumption, production, and net kwh in each time-of-use period. print them
    print ()
    consumption = getStats(start, end, isForProduction=False)
    production = getStats(start, end, isForProduction=True)
    net = map(sub, consumption, production)
    printStats('net', *net)
