import re
import dateparser
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

    domains  = set( map( lambda d: d.replace('www.', ''), domains))

    if domains:
        data = filter( lambda d: '{uri.netloc}'.format( uri= urlparse( d['url'] ) ).replace('www.', '') in domains, data )
    else:
        print 'No domains given for filtering!'

    return data

def counts_author( data ):

    if len(data) == 0:
        print "Dataset empty."
        return

    authors = map( lambda d: d['creator'], data )

    author_counts = Counter(authors)

    total_count = len( author_counts.keys() )

    print 'Authors found in data:', total_count

    print 'Entry counts by author'

    for author, count in author_counts.most_common(total_count):
        print '-', author, count

def counts_domain( data ):

    if len(data) == 0:
        print "Dataset empty."
        return

    domains = map( lambda d: '{uri.netloc}'.format( uri= urlparse( d['url'] ) ).replace('www.', ''), data )

    domain_counts = Counter(domains)

    total_count = len( domain_counts.keys() )

    print 'Domains found in data:', total_count

    print 'Entry counts by domain:'

    for domain, count in domain_counts.most_common(total_count):
        print '-', domain, count
