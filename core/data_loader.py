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
                    d['timestamp'] = dateparser.parse( d['_created_time'] ) ## should take care of the various formats
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

                d['timestamp'] = dateparser.parse( min( d['_datetime_list'] ), ) ## should take care of the various formats

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
                    d['timestamp'] = dateparser.parse( d['_created_at'] ) ## should take care of the various formats
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


def load_futusome( query, data_folder = 'futusome/', api_key = '', check_document_count = False, override_cache = False ):

    data = []

    path = __DATA_DIR + data_folder

    if not os.path.exists( path ):
        os.makedirs( path )

    query_string = 'https://api.futusome.com/api/searches.json?'

    query_string += '&api_search[query]=' + query

    unharmonized_data = load_unharmonized_futusome_data( query_string, api_key, path, check_document_count, override_cache )

    if not unharmonized_data: return data

    for d in unharmonized_data['documents']:

        d = __harmonize_data( d['fields'], 'futusome' )

        try:
            d['creator'] = d['_author']
        except Exception, e:
            d['broken']['creator'] = e

        try:
            d['timestamp'] = dateparser.parse(d['_published'])
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

        url_errors = []
        try:
            d['url'] = d['_blog_id']
        except Exception, e:
            url_errors.append(e)
            d['broken']['url'] = url_errors

        if d['url'] == '':
            try:
                d['url'] = d['_url']
            except Exception, e:
                url_errors.append(e)
                d['broken']['url'] = url_errors

        try:
            d['source_detail'] = d['_type']
        except Exception, e:
            d['broken']['source_detail'] = e

        if '_forum_post_id' in d:
            d['_id'] = d['_forum_post_id']
        elif '_twitter_retweet_id' in d:
            d['_id'] = 'twitter_' + d['_twitter_retweet_id']
        elif '_facebook_id' in d:
            d['_id'] = 'facebook_' + d['_facebook_id']
        elif '_twitter_tweet_id' in d:
            d['_id'] = 'twitter_' + d['_twitter_tweet_id']
        else:
            ## make uniq ID ourself
            text =  d['_url'].encode('ascii', 'ignore') + str( d['timestamp'] ) + d['text_content'].encode('ascii', 'ignore')
            d['_id'] = 'created_id_' + hashlib.md5( text ).hexdigest()

        data.append(d)

    return data


def load_unharmonized_futusome_data( query_string, api_key, data_path, check_document_count, override_cache ):

    if check_document_count:
        r = requests.get( query_string + '&api_key=' + api_key + '&api_search[limit]=1' )
        r =  r.json()
        print('Total document count: ' + str(r['count']))
        return

    query_base = 'https://api.futusome.com/api/searches.json?'

    unharmonized_data = {}

    cache_file = query_string.replace(query_base, '')
    cache_file = cache_file.replace('&api_search[query]=', '')

    if not override_cache:

        print( "Checking local data path for cached data..." )

        for f in os.listdir( data_path ):

            if cache_file == f.replace('.json', ''):
                print("Data returned from " + data_path)

                with open( data_path + '/' + f ) as current_file:
                    unharmonized_data = json.load( current_file )

    if api_key and not unharmonized_data:

        print( "Data not returned from cache. Querying Futusome api..." )

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

            r = requests.get( query_string + time + '&api_key=' + api_key + '&api_search[limit]=5000&api_search[sort]=indexed.at' )
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

        json.dump( unharmonized_data , open(  data_path + '/' + cache_file + '.json', 'w' ) )
        print('Data saved to ' + data_path + '/' + cache_file + '.json')

    return unharmonized_data
