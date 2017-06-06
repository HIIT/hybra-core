from __future__ import division, print_function

import datetime

from timeline import module_timeline

from collections import *

from urlparse import urlparse

def describe( data ):
    if len(data) == 0:
        print( "Dataset empty." )
        return

    print( "Entries together", len(data) )
    print( "Number of different authors", len( set( map( lambda d: d['creator'], filter( lambda d: d['creator'] is not '', data ) ) ) ) )

    ## remove dates which can not be true
    date_ok = filter( lambda d: d['timestamp'] is not '', data )
    date_ok = filter( lambda d: d['timestamp'] > datetime.datetime(1970,1,1,23,59), date_ok )

    print( "First post", min( map( lambda d: d['timestamp'], date_ok ) ) )
    print( "Last post", max( map( lambda d: d['timestamp'], date_ok  ) ) )

    print("Data sources")

    ## todo: reimplement?
    counter = defaultdict( int )

    for post in data:
        counter[ post['source_detail'] ] += 1

    for name, count in counter.items():
        print( '-', name, count )

    return module_timeline.create_timeline( datasets = [date_ok] )

def author_counts( data ):

    if len(data) == 0:
        print( "Dataset empty." )
        return

    authors = map( lambda d: d['creator'], data )

    author_counts = Counter(authors)

    total_count = len( author_counts.keys() )

    print('Authors found in data:', total_count)

    print('Entry counts by author')

    for author, count in author_counts.most_common(total_count):
        print('-', author, count)

def domain_counts( data ):

    if len(data) == 0:
        print( "Dataset empty." )
        return

    domains = map( lambda d: '{uri.netloc}'.format( uri= urlparse( d['url'] ) ), data )

    domain_counts = Counter(domains)

    total_count = len( domain_counts.keys() )

    print('Domains found in data:', total_count)

    print('Entry counts by domain:')

    for domain, count in domain_counts.most_common(total_count):
        print('-', domain, count)

if __name__ == '__main__':

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print( function_name )
            f =  getattr( data_loader, function_name )
            data = f()
            describe( data )
