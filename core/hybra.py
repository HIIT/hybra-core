import data_loader
import descriptives
import network as module_network
import timeline as module_timeline
import wordclouds as module_wordclouds

from IPython.core.display import display, HTML, Javascript

import os
import re
import json

import codecs
from string import Template

__sources = dir( data_loader )
__sources = filter( lambda x: x.startswith('load_') , __sources )
__sources = map( lambda x: x[5:], __sources )

def set_data_path( path ):
    data_loader.__DATA_DIR = path

    ## when data path is set, automatically print out the versions
    for folder in os.listdir( path ):
        if( os.path.isdir( path + folder ) ):
            data_loader._version( folder )

    ## TOTALLY UNRELATED BUT LETS USE THIS TO INIT THE D3JS TOO
    ## check if there is any way to not use exernal cloud d3js
    ## import os
    ## path = os.path.dirname(os.path.abspath(__file__))
    ## return Javascript( open( path + '/js/d3/d3.js' ).read() )
    return HTML('<p><script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.js"></script>Data science OK!</p>')

def data_path():
    return data_loader.__DATA_DIR

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
    return HTML( descriptives.describe( data ) )

def timeline( data ):
    return HTML( module_timeline.create_timeline( data ) )

def network( data ):
    return HTML( module_network.create_network(data) )

def wordcloud( data ):
    module_wordclouds.create_wordcloud( data )
