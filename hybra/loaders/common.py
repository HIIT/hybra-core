#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import sys
import re
import hashlib

from datetime import datetime, timedelta

import locale
locale.setlocale(locale.LC_ALL, 'C')

import dateparser
## try a few common formats first, then fall back to date parser (slow)
def _text_to_datetime( text ):
    try:# 2017-06-30 23:13:53
        return datetime.datetime.strptime( text , '%Y-%m-%d %H:%M:%S')
    except:
        pass

    try: # 2017-02-06T19:52:10+0000
        return datetime.datetime.strptime( text , '%Y-%m-%dT%H:%M:%S%z')
    except:
        pass

    return dateparser.parse( text , settings={'RETURN_AS_TIMEZONE_AWARE': False} )

def _version( folder ):

    print( "Data in folder", folder )

    try:

        from git import Repo

        r = Repo( __DATA_DIR + folder )
        print( "\t Version", r.heads.master.commit )
        print( "\t Updated on", r.heads.master.commit.authored_datetime )

    except:

        print( "\t Data is not stored in a repo. Data might not be up-to-date!" )


def __init_harmonize_data( data, data_type, common_data_keys ):

    import dateparser

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
    harmonized_data['links_domains'] = []
    harmonized_data['broken'] = {}

    for key, value in common_data_keys.items():
        try:
            if type(key) is tuple:
                harmonized_data[value] += harmonized_data[key[0]][key[1]]
            else:
                harmonized_data[value] += harmonized_data[key] + ' '

            harmonized_data[value] = harmonized_data[value].strip()

        except Exception as e:
            harmonized_data['broken'][value] = e

    if not harmonized_data['timestamp']:
        harmonized_data['timestamp'] = '1970-01-01 00:00:00'

    harmonized_data['timestamp'] = _text_to_datetime( harmonized_data['timestamp'] )

    return harmonized_data

def __post_harmonize_data( d ):

    from helpers import urls

    d['links'] += urls.extract( d['text_content'] )
    d['links_domains'] = urls.domains( d['links'] )

    if '_id' in d:
        d['id'] = d['source'].lower() + '_' + d['_id']
    else: ## compute an ID for the object

        _url = ''
        if '_url' in d:
            _url = d['_url']

        text = d['text_content']

        content =  _url + str(d['timestamp']) + text
        d['id'] = d['source'].lower() + '_' + hashlib.md5(content.encode()).hexdigest()

    return d
