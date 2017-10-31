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

def load( terms = ['.json'], data_dir = '', folder = 'news/' ):

    import dateparser

    path = data_dir + folder

    for dirpath, subdirs, files in os.walk(path):

        for f in files:

            f = os.path.join( dirpath, f )

            if any( term in f for term in terms ):

                for d in json.load( open( f ) ):

                    common_data_keys = {'_author' : 'creator',
                                        '_title' : 'text_content',
                                        '_ingress' : 'text_content',
                                        '_text' : 'text_content',
                                        '_url' : 'url',
                                        '_domain' : 'source_detail'}

                    d = common.__init_harmonize_data( d, 'news_media', common_data_keys )

                    ## ensure data is always in a list
                    if isinstance( d['_datetime_list'] , str) or isinstance( d['_datetime_list']  , unicode):
                        d['_datetime_list'] = [ d['_datetime_list'] ]

                    try:
                        d['timestamp'] = dateparser.parse( min( d['_datetime_list'] ), ) ## should take care of the various formats
                    except Exception, e:
                        d['broken']['_datetime_list'] = e

                    d['images'] = d['_images']

                    d = common.__post_harmonize_data( d )
                    yield d
