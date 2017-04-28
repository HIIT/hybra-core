import data_loader
import exporter
import descriptives
from network import module_network
from timeline import module_timeline
import wordclouds as module_wordclouds

from analysis.runr import runr

from IPython.core.display import display, HTML, Javascript

import os
import re
import json
import random

import codecs
from string import Template

__sources = dir( data_loader )
__sources = filter( lambda x: x.startswith('load_') , __sources )
__sources = map( lambda x: x[5:], __sources )

def set_data_path( path ):
    """ Sets the path where the data is stored. Relative to where you run your Python.
        :param path: Where the data is stored

        :Example:

        ``hybra.set_data_path('.') ## search for data from the current folder
        hybra.set_data_path('~/Documents/data/hybra-data') ## data in folder Documents/data/hybra-data``
    """

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
    """ Returns the existing data path.
    """

    return data_loader.__DATA_DIR

def data_sources():
    """ Lists possible data sources hybra core can parse.
    """

    return __sources

def data( source, **kwargs ):
    """ Load data of type `source` using the parser for that data.
        The `**kwargs` are data loader spesific, but often include parameters such as folder.
        See :ref:`data_loader` for details of `**kwargs`

        :param source: type of data loaded. Can be `facebook`, `media`, `twitter`.

        :Example:

        ``hybra.data('media', folder = 'yle') ## load yle-data from the subfolder YLE in your data folder.``
    """

    if source not in __sources:
        raise NameError('Unknown media type')

    load = getattr( data_loader, 'load_' + source )

    return load( **kwargs )

def filter_from_text( data, text = [], substrings = True ):
    """ Only choose parts of data which have certain words, given in parameter `text`.

    :param data: list of data entries.
    :param text: list of words looked for. This is *inclusive* all the words need to be in the text to qualify.
    :param substrings: if we accept texts which match all words or texts which has all words. Default behavior is to accept based on match.
    For example `hybra.filter_from_text( example, ['cat', 'dog'])` would match text `cats and dogs are nice`, whereas `hybra.filter_from_text( example, ['cat', 'dog'], substrings = False )` would not.
    """

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
    """Describe the dataset `data`, showing the amount of posts, number of authors, historical data and more detailed data sources.

    :param data: list of data entries.
    """

    return HTML( descriptives.describe( data ) )

def timeline( **kwargs ):
    """Draws a timeline the dataset `data`.

    :todo: check kwargs

    :param data: list of data entries.
    """

    return HTML( module_timeline.create_timeline( **kwargs ) )

def network( data ):
    """Draws a network the dataset `data`.

    :todo: check kwargs

    :param data: list of data entries.
    """

    return HTML( module_network.create_network(data) )

def wordcloud( data, **kwargs ):
    """Draws a wordcloud the dataset `data`.

    :todo: check kwargs

    :param data: list of data entries.
    """

    module_wordclouds.create_wordcloud( data, **kwargs )

def analyse( script, **kwargs ):

    globalenv = None
    if 'previous' in kwargs:
        globalenv = kwargs[ g ]
        del kwargs['previous']

    return runr( script, globalenv, **kwargs )

def export( data, file_path ):
    """Export the dataset `data` in common format to the given file format.

    :param data: List of data entries to be exported.
    :param file_path: Path to output file. Recognizes output format from file extension in the path.
    """

    file_type = file_path.split('.')[-1]

    try:
        file_exporter = getattr( exporter, 'export_' + file_type )

        file_exporter( data, file_path )

    except Exception, e:
        print(repr(e))
        print("File export failed. Supported file types:")

        for f_type in filter( lambda x: x.startswith('export_') , dir( exporter ) ):
            print( '.' + f_type.replace('export_', '') )

def sample(data, size, seed = None, export_file = None):
    """Takes a random sample of the dataset `data`. Optionally exports the sample to file.

    :param data: List of the data entries to be exported.
    :param size: An integer value specifying the sample size.
    :param seed: Seed to use in randomization. Defaults to None.
    :param export_file: Path to output file. Defaults to None.
    """

    if seed:
        random.seed(seed)

    data_sample = random.sample(data, size)

    if export_file:
        export( data_sample, export_file )

    return random.sample(data, size)
