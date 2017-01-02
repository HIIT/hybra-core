import data_loader
import re
import descriptives
import network as module_network
import timeline as module_timeline
import wordclouds as module_wordclouds

__sources = dir( data_loader )
__sources = filter( lambda x: x.startswith('load_') , __sources )
__sources = map( lambda x: x[5:], __sources )

def data_sources():
    return __sources

def data( type, **kwargs ):

    if type not in __sources:
        raise NameError('Unknown media type')

    load = getattr( data_loader, 'load_' + type )

    return load( **kwargs )

def filter_from_text( data, text = [], substrings = True ):
    filtered_data = []

    for d in data:
        if substrings:
            if all( string.lower() in d['text_content'].lower() for string in text ):
                filtered_data.append( d )
        else:
            words = re.findall(r'\w+', d['text_content'].lower(), re.UNICODE)
            if all( string.lower() in words for string in text ):
                filtered_data.append( d )

    return filtered_data

def describe( data ):
    descriptives.describe( data )

## igrap plotting utilities

def timeline( data ):
    module_timeline.create_timeline( data )

def network( data ):
    module_network.create_network( data )

def wordcloud( data ):
    module_wordclouds.create_wordcloud( data )
