import re
from urlparse import urlparse
from collections import Counter

def filter_by_text( data, text = [], substrings = True, inclusive = True ):

    filtered_data = []

    if text:
        text = map( lambda t: t.decode('utf8'), text)
    else:
        print('No text given for filtering!')
        return data

    for d in data:
        if substrings:
            if inclusive:
                if all( string.lower() in d['text_content'].lower() for string in text ):
                    filtered_data.append( d )
            else:
                if any( string.lower() in d['text_content'].lower() for string in text ):
                    filtered_data.append( d )
        else:
            words = re.findall(r'\w+', d['text_content'].lower(), re.UNICODE)
            if inclusive:
                if all( string.lower() in words for string in text ):
                    filtered_data.append( d )
            else:
                if any( string.lower() in words for string in text ):
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
        print 'No dates given for filtering!'

    return data

def filter_by_author( data, authors = [] ):

    authors = set( map( lambda a: a.decode('utf8'), authors) )

    if authors:
        data = filter( lambda d: d['creator'] in authors, data )
    else:
        print 'No authors given for filtering!'

    return data

def filter_by_domain( data, domains = [] ):

    import tldextract

    domains  = set( map( lambda d: d.replace('www.', ''), domains))

    if domains:
        data = filter( lambda d: '.'.join( tldextract.extract( d['url'] )[-2:] ) in domains, data )
    else:
        print 'No domains given for filtering!'

    return data
