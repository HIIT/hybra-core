import json
import os
import sys

#import dateparser
from datetime import datetime

__DATA_DIR = '../hybra-data-test1/' ## by default the data comes here

try:
    from git import Repo

    r = Repo( __DATA_DIR )

    print "Analysis done on data version", r.heads.master.commit,"updated on", r.heads.master.commit.authored_datetime
    print "Store this for future reference."

except:

    print "Data direcotry is not a git repo. Data might not be up-to-date!"

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

def load_facebook( terms = ['data_'], data_folder = 'facebook/' ): ## todo: better filtering

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            #print json.load( open( __DATA_DIR + f ) ).keys()

            data += json.load( open( path + f ) )['feed']

    return harmonize_data( data )

def load_media( terms = ['.json'], data_folder = 'media/' ):

    import pickle ## for now, using picke - JSON later on

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            d = pickle.load( open( path + f ) )

            ## TBA: change to standart format correctly
            d['date'] = min( d['datetime_list'] )
            d['creator'] = d['author']
            d['message'] = d['title'] + ' ' + d['ingress'] + ' ' + d['text']

            data.append( d )

    return data
