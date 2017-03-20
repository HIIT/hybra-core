from __future__ import division, print_function

import json
import os
import sys
import re
import requests

#import dateparser
from datetime import datetime

__DATA_DIR = '../hybra-data-test1/' ## by default the data comes here

def _version( folder ):

    print( "Data in folder", folder )

    try:

        from git import Repo

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
    harmonized_data['timestamp'] = datetime.strptime( '1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S' )
    harmonized_data['text_content'] = ''
    harmonized_data['url'] = ''
    harmonized_data['source_detail'] = ''
    harmonized_data['images'] = []
    harmonized_data['links'] = []
    harmonized_data['broken'] = {}

    return harmonized_data


def load_facebook( terms = ['.json'], data_folder = 'facebook/' ): ## todo: better filtering

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            dump = json.load( open( path + f ) )

            source_detail = dump['name']

            for d in dump['feed']:

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
                if '_attachments' in d and 'data' in d['_attachments']:
                    for attachment in d['_attachments']['data']:
                        if attachment['type'] == 'photo':
                            attachments.append( attachment['media']['image']['src']  )

                d['images'] = attachments

                d['links'] = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', d['text_content'] )

                d['source_detail'] = source_detail

                data.append( d )

    return data


def load_media( terms = ['.json'], data_folder = 'media/' ):

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            for d in json.load( open( path + f ) ):

                d = __harmonize_data( d, 'news_media' )

                d['creator'] = d['_author']

                ## ensure data is always in a list
                if isinstance( d['_datetime_list'] , str) or isinstance( d['_datetime_list']  , unicode):
                    d['_datetime_list'] = [ d['_datetime_list'] ]

                d['timestamp'] = datetime.strptime( min( d['_datetime_list'] ), '%Y-%m-%d %H:%M:%S' ) ## todo: works for YLE, don't know of others
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


def load_futusome( query, data_folder = 'futusome/', api_key = '', limit = 1000, **kwargs ):

    data = []

    path = __DATA_DIR + data_folder

    if not os.path.exists( path ):
        os.makedirs( path )

    query_string = 'https://api.futusome.com/api/searches.json?'

    query_string += '&api_search[query]=' + query

    for key, value in kwargs.items():
        query_string += '&api_search[' + key + ']=' + str( value )

    unharmonized_data = load_unharmonized_futusome_data( query_string, api_key, path, limit )

    if not unharmonized_data: return data

    for d in unharmonized_data['documents']:

        d = __harmonize_data( d['fields'], 'futusome' )

        try:
            d['creator'] = d['_author']
        except Exception, e:
            d['broken']['creator'] = e

        try:
            d['timestamp'] = datetime.strptime( d['_published'], '%Y-%m-%d %H:%M:%S +0000' )
        except Exception, e:
            d['broken']['timestamp'] = e

        d['text_content'] = ''
        text_content_errors = []
        try:
            d['text_content'] += d['_name'] + ' '
        except Exception, e:
            text_content_errors.append(e)
            d['broken']['text_content'] = text_content_errors

        try:
            d['text_content'] += d['_text']
        except Exception, e:
            text_content_errors.append[e]
            d['broken']['text_content'] = text_content_errors

        try:
            d['url'] = d['_blog_id'] or d['_url']
        except Exception, e:
            d['broken']['url'] = e

        try:
            d['source_detail'] = d['_type']
        except Exception, e:
            d['broken']['source_detail'] = e

        data.append(d)

    return data


def load_unharmonized_futusome_data( query_string, api_key, data_path, limit ):

    query_base = 'https://api.futusome.com/api/searches.json?'

    unharmonized_data = []

    print( "Checking local data path for cached data..." )

    for f in os.listdir( data_path ):

        if query_string.replace(query_base, '') == f.replace('.json', ''):
            print("Data returned from cache.")

            with open( data_path + '/' + f ) as current_file:
                unharmonized_data = json.load( current_file )

    if api_key and not unharmonized_data:

        print( "Data not in cache. Querying Futusome api..." )

        offset = 1

        if limit > 5000:
            offset = int( limit / 5000 ) + 1
            limit = 5000

        unharmonized_data = {}
        unharmonized_data['documents'] = []

        for ofs in range( offset ):

            r = requests.get(query_string + '&api_key=' + api_key + '&api_search[limit]=' + str( limit ) + '&api_search[offset]=' + str( limit * offset + 1 ) )

            r =  r.json()

            unharmonized_data['metadata'] = {
                'count' : r['count'],
                'query' : r['query']
            }

            unharmonized_data['documents'] += r['documents']

        cache_file = query_string.replace(query_base, '')

        json.dump( unharmonized_data , open(  data_path + '/' + cache_file + '.json', 'w' ) )

    return unharmonized_data
