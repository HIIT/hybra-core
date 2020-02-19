from __future__ import print_function
import re
from collections import Counter

def filter_by_text( data, text = [], substrings = True, inclusive = True ):

    filtered_data = []

    terms = [ term.lower() for term in text ]

    for d in data:
        if substrings:
            if inclusive:
                if all( term in d['text_content'].lower() for term in terms ):
                    filtered_data.append( d )
            else:
                if any( term in d['text_content'].lower() for term in terms ):
                    filtered_data.append( d )
        else:
            words = re.findall(r'\w+', d['text_content'].lower() )
            if inclusive:
                if all( term in words for term in terms ):
                    filtered_data.append( d )
            else:
                if any( term in words for term in terms ):
                    filtered_data.append( d )

    return filtered_data

def filter_by_datetime( data, after = '', before = '' ):

    import dateparser

    after = dateparser.parse(after)
    before = dateparser.parse(before)

    if (after != None) & (before != None):
        data = filter( lambda d: (d['timestamp'] > after) & (d['timestamp'] < before), data )
    elif after:
        data = filter( lambda d: d['timestamp'] > after, data )
    elif before:
        data = filter( lambda d: d['timestamp'] < before, data )
    else:
        print('No dates given for filtering!')

    return list(data)

def filter_by_author( data, authors = [] ):

    authors = set( authors )

    if authors:
        data = filter( lambda d: d['creator'] in authors, data )
    else:
        print('No authors given for filtering!')

    return list(data)

def filter_by_domain( data, domains = [] ):

    import tldextract

    domains  = set( map( lambda d: d.replace('www.', ''), domains))

    if domains:
        data = filter( lambda d: '.'.join( tldextract.extract( d['url'] )[-2:] ) in domains, data )
    else:
        print('No domains given for filtering!')

    return list(data)
