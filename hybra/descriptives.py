from __future__ import division, print_function
import datetime
from collections import *

import pprint
import core
pp = pprint.PrettyPrinter(indent=1)

def describe( data ):

    import types

    if isinstance( data, types.GeneratorType ):
        data = list( data )

    if not data: return "Dataset empty."

    from timeline import module_timeline

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

    print( 'Data structure' )
    pp.pprint( keys( data ) )


    if core.IPYTHON_NOTEBOOK:
        from IPython.core.display import HTML, display
        module_timeline.create_timeline( datasets = [date_ok] )

def keys( data ):

    res = []

    ## fake a bit, as different data entries can have different keys
    for entry in data[0:50]:
        res.append( _keys( entry ) )

    ## search for the longest string representation as it most likely has most information

    return sorted( res, key = lambda x : len(str(x)), reverse = True)[0]

def _keys( entry ):

    if isinstance( entry, list ):
        if len( entry ) > 0:
            return [ _keys( entry[0] ) ]
        return []

    if isinstance( entry, dict ):
        out = {}

        for k, v in entry.items():
            out[str(k)] = _keys( v )

        return out

    if isinstance( entry, str) or isinstance( entry, unicode):
        return 'text'

    if isinstance( entry, float) or isinstance( entry, int):
        return 'number'

    if isinstance( entry, datetime.datetime ):
        return 'time'

    return str( type( entry ) )
