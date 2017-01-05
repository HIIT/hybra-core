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

    harmonized_data = {}

    for key in data.keys():
        harmonized_data['_' + key] = data[key]

    harmonized_data['source'] = data_type
    harmonized_data['creator'] = ''
    harmonized_data['timestamp'] = ''
    harmonized_data['text_content'] = ''
    harmonized_data['url'] = ''
    harmonized_data['source_detail'] = ''
    harmonized_data['images'] = []
    harmonized_data['links'] = []
    harmonized_data['broken'] = {}

    return harmonized_data

def load_facebook( terms = ['data_'], data_folder = 'facebook/' ): ## todo: better filtering

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            unharmonized_data = json.load( open( path + f ) )['feed']

            for d in unharmonized_data:

                d = __harmonize_data( d, 'facebook' )

                try:
                    d['creator'] = d['_from']['name']
                except Exception, e:
                    d['broken']['creator'] = e

                try:
                    #d['timestamp'] = dateparser.parse( d['created_time'] ) ## should take care of the various formats
                    d['timestamp'] = datetime.strptime( d['_created_time'].replace( 'T', ' ' ).replace( '+0000', '' ), '%Y-%m-%d %H:%M:%S' )
                except Exception, e:
                    d['broken']['timestamp'] = e

                try:
                    d['text_content'] = d['_message']
                except Exception, e:
                    d['broken']['text_content'] = e

                d['url'] = 'https://www.facebook.com/' + d['_id']

                data.append( d )

    return data

def load_media( terms = ['.json'], data_folder = 'media/' ):

    import pickle ## for now, using picke - JSON later on

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            d = pickle.load( open( path + f ) )

            d = __harmonize_data( d, 'news_media' )

            d['creator'] = d['_author']
            d['timestamp'] = min( d['_datetime_list'] )
            d['text_content'] = d['_title'] + ' ' + d['_ingress'] + ' ' + d['_text']
            d['url'] = d['_url']

            try:
                d['source_detail'] = d['_domain']
            except Exception, e:
                d['broken']['source_detail'] = e

            d['images'] = d['_images']

            data.append(d)

    return data
