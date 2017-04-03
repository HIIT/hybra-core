from __future__ import division, print_function

import json
import os
import sys
import re
import requests
import hashlib

import dateparser
from datetime import datetime
from datetime import timedelta

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


def __harmonize_data( data, data_type, common_data_keys ):

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

    for key, value in common_data_keys.items():
        try:
            if type(key) is tuple:
                harmonized_data[value] += harmonized_data[key[0]][key[1]]
            else:
                harmonized_data[value] += harmonized_data[key] + ' '

            harmonized_data[value] = harmonized_data[value].strip()

        except Exception, e:
            harmonized_data['broken'][value] = e

    if not harmonized_data['timestamp']:
        harmonized_data['timestamp'] = '1970-01-01 00:00:00'

    harmonized_data['timestamp'] = dateparser.parse( harmonized_data['timestamp'] )

    return harmonized_data


def load_facebook( terms = ['.json'], data_folder = 'facebook/' ): ## todo: better filtering

    data = []

    path = __DATA_DIR + data_folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            dump = json.load( open( path + f ) )

            source_detail = dump['name']

            for d in dump['feed']:

                common_data_keys = {('_from', 'name') : 'creator',
                                    '_created_time' : 'timestamp',
                                    '_message' : 'text_content'}

                d = __harmonize_data( d, 'facebook', common_data_keys )

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

                common_data_keys = {'_author' : 'creator',
                                    '_title' : 'text_content',
                                    '_ingress' : 'text_content',
                                    '_text' : 'text_content',
                                    '_url' : 'url',
                                    '_domain' : 'source_detail',
                                    '_images' : 'images'}

                d = __harmonize_data( d, 'news_media', common_data_keys )

                ## ensure data is always in a list
                if isinstance( d['_datetime_list'] , str) or isinstance( d['_datetime_list']  , unicode):
                    d['_datetime_list'] = [ d['_datetime_list'] ]

                try:
                    d['timestamp'] = dateparser.parse( min( d['_datetime_list'] ), ) ## should take care of the various formats
                except Exception, e:
                    d['broken']['_datetime_list'] = e

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

                unharmonized_data = []

                with open( path + f ) as current_file:
                    unharmonized_data = json.load( current_file )

                for d in unharmonized_data:

                    common_data_keys = {('_user', 'screen_name') : 'creator',
                                        '_created_at' : 'timestamp',
                                        '_text' : 'text_content'}

                    d = __harmonize_data( d, 'twitter', common_data_keys )

                    try:
                        d['url'] = 'https://www.twitter.com/statuses/' + d['_id_str']
                    except Exception, e:
                        d['broken']['url'] = e

                    data.append(d)

    return data


def load_futusome( query, data_folder = 'futusome/', api_key = '', check_document_count = False, override_cache = False ):

    """ Checks local data folder for files matching the given query and returns them if a match is found.
        If no local data is found and an API key is given, Futusome API is queried.

        :param query: String with which data is queried.
        :param data_folder: Local data folder as a string.
        :param api_key: API key as a string for querying Futusome API.
        :param check_document_count: Boolean. Defaults to False. If True, method checks Futusome API for document count returned by the given query. If False, loads the documents and saves them.
        :param override_cache: Boolean. Defaults to False. If True, always queries Futusome and saves the data over local files. If False, checks local cache for data.
    """

    data = []

    path = __DATA_DIR + data_folder

    if not os.path.exists( path ):
        os.makedirs( path )

    query_base = 'https://api.futusome.com/api/searches.json?&api_search[query]='

    cache_file = query.replace('/', '_') # Slashes not allowed in filenames


    # If just checking document count, query for only one document
    if check_document_count:
        r = requests.get( query_base + query + '&api_key=' + api_key + '&api_search[limit]=1' )
        r =  r.json()
        print('Total document count: ' + str(r['count']))
        return


    unharmonized_data = {}


    # Check if data matching the query is cached in the data path
    if not override_cache:

        print( "Checking local data path for cached data..." )

        for f in os.listdir( path ):

            if cache_file == f.replace('.json', ''):
                print("Data returned from " + path)

                with open( path + '/' + f ) as current_file:
                    unharmonized_data = json.load( current_file )


    # If data not found in cache, query Futusome API
    if api_key and not unharmonized_data:

        print( "Data not returned from cache. Querying Futusome API..." )

        documents = []

        collected = 0
        jump = timedelta(365*25) ## high enough

        while True:

            ## min-range

            time = ''

            if collected:
                ## start to do jumps
                max_date = documents[-1]['fields']['indexed']
                max_date = datetime.strptime( max_date , "%Y-%m-%d %H:%M:%S +0000")
                min_date = max_date - jump
                max_date = str( ( int( max_date.strftime('%s') ) + 7200 ) * 1000 - 1 ) # correct for UTC time
                min_date = str( int( min_date.strftime('%s') ) * 1000 )
                time = ' AND indexed.at:['  + min_date + ' TO ' + max_date + ']' ## could also be indexed at? is it faster?

            r = requests.get( query_base + query + time + '&api_key=' + api_key + '&api_search[limit]=5000&api_search[sort]=indexed.at' )
            r =  r.json()

            if 'error' in r:
                print( r )
                break

            if not collected:
                print( '\tTotal sample is', r['count'] )

            if len( r['documents'] ) == 0:
                print( r ) ## for debug
                break ## everything OK

            documents += r['documents']
            collected += len( r['documents'] )

            print( '\tNow', collected,'documents and at', documents[-1]['fields']['indexed'], 'and going deeper...')

        unharmonized_data = {'documents' : documents}

        # Save data in local cache with the query as filename
        json.dump( unharmonized_data , open(  path + '/' + cache_file + '.json', 'w' ) )
        print('Data saved to ' + path + '/' + cache_file + '.json')


    # If no data found in cache or Futusome, just return
    if not unharmonized_data: return data


    # Harmonize data to common format and return it
    for d in unharmonized_data['documents']:

        common_data_keys = {'_author' : 'creator',
                            '_published' : 'timestamp',
                            '_name' : 'text_content',
                            '_text' : 'text_content',
                            '_url' : 'url',
                            '_blog_id' : 'url',
                            '_type' : 'source_detail'}

        d = __harmonize_data( d['fields'], 'futusome', common_data_keys )

        d['timestamp'] = d['timestamp'].replace(tzinfo = None)

        if '_forum_post_id' in d:
            d['_id'] = d['_forum_post_id']
        elif '_twitter_retweet_id' in d:
            d['_id'] = 'twitter_' + d['_twitter_retweet_id']
        elif '_facebook_id' in d:
            d['_id'] = 'facebook_' + d['_facebook_id']
        elif '_twitter_tweet_id' in d:
            d['_id'] = 'twitter_' + d['_twitter_tweet_id']
        elif '_url' in d:
            ## make uniq ID ourself
            text =  d['_url'].encode('ascii', 'ignore') + str( d['timestamp'] ) + d['text_content'].encode('ascii', 'ignore')
            d['_id'] = 'created_id_' + hashlib.md5( text ).hexdigest()
        else:
           text =  str( d['timestamp'] ) + d['text_content'].encode('ascii', 'ignore')
           d['_id'] = 'created_id_' + hashlib.md5( text ).hexdigest()

        data.append(d)

    return data
