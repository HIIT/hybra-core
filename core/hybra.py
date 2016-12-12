import data_loader
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

def describe( data ):
    descriptives.describe( data )

## igrap plotting utilities

def timeline( data ):
    module_timeline.create_timeline( data )

def network( data ):
    module_network.create_network( data )

def wordcloud( data ):
    module_wordclouds.create_wordcloud( data )
