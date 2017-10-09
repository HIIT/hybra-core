#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import json
import os
import sys
import re
import hashlib
import unicodedata

from datetime import datetime, timedelta

import common


def load( query, data_dir = '', folder = 'futusome/', api_key = '', check_document_count = False, override_cache = False ):

    """ Checks local data folder for files matching the given query and returns them if a match is found.
        If no local data is found and an API key is given, Futusome API is queried.

        :param query: String with which data is queried.
        :param data_folder: Local data folder as a string.
        :param api_key: API key as a string for querying Futusome API.
        :param check_document_count: Boolean. Defaults to False. If True, method checks Futusome API for document count returned by the given query. If False, loads the documents and saves them.
        :param override_cache: Boolean. Defaults to False. If True, always queries Futusome and saves the data over local files. If False, checks local cache for data.
    """

    import requests
    import pytz

    path = data_dir + folder

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
        tz = pytz.timezone("Europe/Helsinki") ## for timezone correction

        while True:

            ## min-range

            time = ''

            if collected:
                ## start to do jumps
                max_date = documents[-1]['fields']['indexed']
                max_date = datetime.strptime( max_date , "%Y-%m-%d %H:%M:%S +0000")
                min_date = max_date - jump

                utc_correct = int( tz.localize(max_date).utcoffset().total_seconds() ) # correct for UTC time

                max_date = str( ( int( max_date.strftime('%s') ) + utc_correct ) * 1000 - 1 )
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
    if not unharmonized_data: return

    # Harmonize data to common format and return it
    for d in unharmonized_data['documents']:

        common_data_keys = {'_author' : 'creator',
                            '_published' : 'timestamp',
                            '_name' : 'text_content',
                            '_text' : 'text_content',
                            '_url' : 'url',
                            '_blog_id' : 'url',
                            '_type' : 'source_detail'}

        d = common.__init_harmonize_data( d['fields'], 'futusome', common_data_keys )

        d['timestamp'] = d['timestamp'].replace(tzinfo = None)

        url_regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

        # Hack to fix backtracking issue with the regex, should be fixed in the regex itself
        text_for_url_parsing = re.sub('\.{2,}', '', d['text_content'])

        d['links'] = re.findall( url_regex, text_for_url_parsing )

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

        ## reharmonize
        d = common.__post_harmonize_data( d )
        yield d
