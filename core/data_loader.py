from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import sys
import re

from git import Repo

#import dateparser
from datetime import datetime

__DATA_DIR = '../hybra-data-test1/' ## by default the data comes here

def _version( folder ):

    print( "Data in folder", folder )

    try:
        r = Repo( __DATA_DIR + folder )
        print( "\t Version", r.heads.master.commit )
        print( "\t Updated on", r.heads.master.commit.authored_datetime )

    except:

        print( "\t Data is not stored in a repo. Data might not be up-to-date!" )


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

                attachments = []
                if 'attachments' in d and 'data' in d['attachments']:
                    for attachment in d['attachments']['data']:
                        if attachment['type'] == 'photo':
                            attachments.append( attachment['media']['image']['src']  )

                d['images'] = attachments

                d['links'] = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', d['text_content'] )



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

def load_twitter( terms = ['data_'], data_folder = 'twitter/' ):

    """This is currently written to deal with data from Twitter's Streaming API.
       The data format for Search API data is slightly different
       and allows some things to be done slightly more conveniently;
       we could write this to work with Streaming API data as well.
    """

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            unharmonized_data = []

            with open( path + f ) as current_file:
                unharmonized_data = json.load( current_file )

            for d in unharmonized_data:

                d = __harmonize_data( d, 'twitter' )

                try:
                    d['creator'] = d['_user']['screen_name']
                except Exception, e:
                    d['broken']['creator'] = e

                try:
                    #d['timestamp'] = dateparser.parse( d['created_time'] ) ## should take care of the various formats

                    ## Assumes that timezone is always +0000, not absolutely sure that this holds
                    d['timestamp'] = datetime.strptime( d['_created_at'], '%a %b %d %H:%M:%S +0000 %Y' )
                except Exception, e:
                    d['broken']['timestamp'] = e

                try:
                    d['text_content'] = d['_text']
                except Exception, e:
                    d['broken']['text_content'] = e

                try:
                    d['url'] = 'https://www.twitter.com/statuses/' + d['_id_str']
                except Exception, e:
                    d['broken']['url'] = e

                data.append(d)

    return data
