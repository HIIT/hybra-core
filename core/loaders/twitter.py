#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import json
import os
import sys
import re
import hashlib

from datetime import datetime, timedelta

import common

def load( terms = ['data_'], data_dir = '', folder = 'twitter/' ):

    """This is currently written to deal with data from Twitter's Streaming API.
       The data format for Search API data is slightly different
       and allows some things to be done slightly more conveniently;
       we could write this to work with Streaming API data as well.
    """

    path = data_dir + folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            with open( path + f ) as current_file:
                unharmonized_data = []
                unharmonized_data = json.load( current_file )

                for d in unharmonized_data:

                    common_data_keys = {('_user', 'screen_name') : 'creator',
                                        '_created_at' : 'timestamp',
                                        '_text' : 'text_content'}

                    d = common.__init_harmonize_data( d, 'twitter', common_data_keys )

                    if '_entities' in d:
                        if 'urls' in d['_entities']:
                            d['links'] = map( lambda u: u['expanded_url'], d['_entities']['urls'] )

                    try:
                        d['url'] = 'https://www.twitter.com/statuses/' + d['_id_str']
                    except Exception, e:
                        d['broken']['url'] = e

                    d = common.__post_harmonize_data( d )

                    yield d
