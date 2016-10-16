import json
import os
import dateparser

__DATA_DIR = '/Users/mnelimar/Documents/data/hybra0/' ## TODO: to be fixed

def harmonize_data( data ):
    ## make dates as date objects
    for d in data:
        d['date'] = dateparser.parse( d['created_time'] ) ## should take care of the various formats
        d['creator'] = d['from']['name']

    return data

def load_facebook( terms = 'data_' ): ## todo: better filtering

    data = []

    for f in os.listdir( __DATA_DIR ):

        if any( term in f for term in terms ):

            data += json.load( open( __DATA_DIR + f ) ).values()

    return harmonize_data( data )
