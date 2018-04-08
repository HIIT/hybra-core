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

def load( terms = ['.json'], data_dir = '', folder = 'facebook/', comments = False ): ## todo: better filtering

    path = data_dir + folder

    for f in os.listdir( path ):

        if f.endswith('.json') and any( term in f for term in terms ):

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

                d['source_detail'] = source_detail + ' thread open'

                d = common.__post_harmonize_data( d )
                yield d

                if comments:

                    for dc in d['_comments']:
                        dc = common.__init_harmonize_data( dc, 'facebook', common_data_keys )
                        dc['url'] = 'https://www.facebook.com/' + dc['_id']

                        attachments = []
                        if '_attachments' in d and 'data' in d['_attachments']:
                            for attachment in d['_attachments']['data']:
                                if attachment['type'] == 'photo':
                                    attachments.append( attachment['media']['image']['src']  )

                        dc['images'] = attachments

                        dc['links'] = []

                        #if '_link' in d:
                        #   dc['links'].append( dc['_link'] )

                        dc['source_detail'] = source_detail

                        dc = common.__post_harmonize_data( dc )
                        yield dc

                        for dc1 in dc['_comments']:

                            dc1 = common.__init_harmonize_data( dc1, 'facebook', common_data_keys )
                            dc1['url'] = 'https://www.facebook.com/' + dc1['_id']

                            attachments = []
                            if '_attachments' in d and 'data' in d['_attachments']:
                                for attachment in d['_attachments']['data']:
                                    if attachment['type'] == 'photo':
                                        attachments.append( attachment['media']['image']['src']  )

                            dc1['images'] = attachments

                            dc1['links'] = []

                            #if '_link' in d:
                            #   dc1['links'].append( dc1['_link'] )

                            dc1['source_detail'] = source_detail

                            dc1 = common.__post_harmonize_data( dc1 )
                            yield dc1
