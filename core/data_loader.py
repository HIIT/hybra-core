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

    print "Data directory is not a git repo. Data might not be up-to-date!"

def __harmonize_data( data ):
    ## make dates as date objects
    data2 = []
    for d in data:

        d = __format_data( d )

        if '_created_time' in d:
           #d['date'] = dateparser.parse( d['created_time'] ) ## should take care of the various formats

           d['timestamp'] = datetime.strptime( d['_created_time'].replace( 'T', ' ' ).replace( '+0000', '' ), '%Y-%m-%d %H:%M:%S' )
           d['creator'] = d['_from']['name']
           data2.append( d )

    return data2

def __format_data( data ):
    formatted_data = {}
    for key in data.keys():
        formatted_data['_' + key] = data[key]

    return formatted_data

def load_facebook( terms = ['data_'], data_folder = 'facebook/' ): ## todo: better filtering

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            data += json.load( open( path + f ) )['feed']

    return __harmonize_data( data )

def load_media( terms = ['.json'], data_folder = 'media/' ):

    import pickle ## for now, using picke - JSON later on

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            d = pickle.load( open( path + f ) )

            ## TBA: change to standart format correctly
            d['timestamp'] = min( d['datetime_list'] )
            d['creator'] = d['author']
            d['text_content'] = d['title'] + ' ' + d['ingress'] + ' ' + d['text']

            data.append( d )

    return data


if __name__ == '__main__':
    data = load_facebook(['nokkahuilu'])
    print data[0].keys()
