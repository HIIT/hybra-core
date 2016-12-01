import json
import os
import sys

#import dateparser
from datetime import datetime

__DATA_DIR = '../data/'

def harmonize_data( data ):
    ## make dates as date objects
    data2 = []
    for d in data:
        if 'created_time' in d:
           #d['date'] = dateparser.parse( d['created_time'] ) ## should take care of the various formats

           d['date'] = datetime.strptime( d['created_time'].replace( 'T', ' ' ).replace( '+0000', '' ), '%Y-%m-%d %H:%M:%S' )
           d['creator'] = d['from']['name']
           data2.append( d )

    return data2

def load_facebook( terms = ['data_'] ): ## todo: better filtering

    data = []

    for f in os.listdir( __DATA_DIR ):

        if any( term in f for term in terms ):

            #print json.load( open( __DATA_DIR + f ) ).keys()

            data += json.load( open( __DATA_DIR + f ) )['feed']

    return harmonize_data( data )
