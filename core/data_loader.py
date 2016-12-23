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

def __harmonize_data( data, data_type ):
    ## make dates as date objects
    data2 = []
    for d in data:

        d = __format_data( d )
        d['source'] = data_type

        if data_type == 'facebook':
            d['creator'] = d['_from']['name'] if '_from' in d else ''
            d['text_content'] = d['_message'] if '_message' in d else ''
            d['url'] = 'https://www.facebook.com/' + d['_id']
            d['source_detail'] = '' # TO DO: add source detail from facebook data

            #d['date'] = dateparser.parse( d['created_time'] ) ## should take care of the various formats
            if 'created_time' in d:
                d['timestamp'] = datetime.strptime( d['_created_time'].replace( 'T', ' ' ).replace( '+0000', '' ), '%Y-%m-%d %H:%M:%S' )
            else:
                d['timestamp'] = ''

        elif data_type == 'news_media':
            d['creator'] = d['_author']
            d['timestamp'] = min( d['_datetime_list'] )
            d['text_content'] = d['_title'] + ' ' + d['_ingress'] + ' ' + d['_text']
            d['url'] = d['_url']
            d['source_detail'] = d['_domain'] if '_domain' in d else ''

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

    return __harmonize_data( data , 'facebook' )

def load_media( terms = ['.json'], data_folder = 'media/' ):

    import pickle ## for now, using picke - JSON later on

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            d = pickle.load( open( path + f ) )
            data.append( d )

    return __harmonize_data( data, 'news_media' )
