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

def load( terms = ['.json'], data_dir = '', folder = 'facebook/' ): ## todo: better filtering

    path = data_dir + folder

    for f in os.listdir( path ):

        if any( term in f for term in terms ):

            dump = json.load( open( path + f ) )

            source_detail = dump['name'] + ' (' + dump['meta']['type'] + ')'

            for d in dump['feed']:

                common_data_keys = {('_from', 'name') : 'creator',
                                    '_created_time' : 'timestamp',
                                    '_message' : 'text_content'}

                d = common.__init_harmonize_data( d, 'facebook', common_data_keys )

                d['url'] = 'https://www.facebook.com/' + d['_id']

                attachments = []
                if '_attachments' in d and 'data' in d['_attachments']:
                    for attachment in d['_attachments']['data']:
                        if attachment['type'] == 'photo':
                            attachments.append( attachment['media']['image']['src']  )

                d['images'] = attachments

                d['links'] = []
                
                if '_link' in d:
                   d['links'].append( d['_link'] )

                d['source_detail'] = source_detail

                d = common.__post_harmonize_data( d )
                yield d
