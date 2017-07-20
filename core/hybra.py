import data_loader
import exporter
import helpers
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

def describe( data ):
    """ Describe the dataset `data`, showing the amount of posts,
        number of authors, historical data and more detailed data sources.

        :param data: list of data entries.
    """

    return display( HTML( descriptives.describe( data ) ) )

def timeline( **kwargs ):
    """ Draws a timeline the dataset `data`.

        :todo: check kwargs

        :param data: list of data entries.
    """

    return display( HTML( module_timeline.create_timeline( **kwargs ) ) )

def network( data ):
    """ Draws a network the dataset `data`.

        :todo: check kwargs

        :param data: list of data entries.
    """

    return display( HTML( module_network.create_network(data) ) )

def wordcloud( data, **kwargs ):
    """ Draws a wordcloud the dataset `data`.

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
    """ Export the dataset `data` in common format to the given file format.
        Recognizes output format from file extension in given file path.

        :param data: List of data entries to be exported.
        :param file_path: Path to output file.
    """

    file_type = file_path.split('.')[-1]

    try:
        file_exporter = getattr( exporter, 'export_' + file_type )

        file_exporter( data, file_path )

    except Exception, e:
        print(repr(e))
        print("File export failed. Supported file types:")

        for f in filter( lambda x: x.startswith('export_') , dir( exporter ) ):
            print( '.' + f.replace('export_', '') )

def sample(data, size, seed = 100, export_file = None):
    """ Takes a random sample of the dataset `data`.
        Optionally exports the sample to file using the hybra module export method.

        :param data: List of the data entries to be exported.
        :param size: An integer value specifying the sample size.
        :param seed: Seed to use in randomization. Defaults to 100.
        :param export_file: Path to output file. Defaults to None.
    """

    random.seed(seed)

    data_sample = random.sample(data, size)

    if export_file:
        export( data_sample, export_file )

    return random.sample(data, size)

def filter_by( data, filter_type, **kwargs ):
    """ Filters the dataset `data` with the filter given in `filter_type`.
        Returns the filtered data if `filter_type` matches a filtering method
        in the modude helpers.

        :todo: check kwargs

        :param data: List of the data entries to be filtered.
        :param filter_type: String giving the filter type to be used.
    """

    try:
        filter_helper = getattr( helpers, 'filter_by_' + filter_type )

        return filter_helper( data, **kwargs )

    except Exception, e:
        print(repr(e))
        print('Data filtering failed. Supported filters:')

        for f in filter(lambda x: x.startswith('filter_by_'), dir(helpers) ):
            print( f.replace('filter_by_', '') )

def counts( data, count_by ):
    """ Counts the occurrences of the feature `count_by` in the dataset `data`.

        :param data: List of the data entries to be counted.
        :param count_by: String giving the feature to be used for counting.

        :Example:

        ``hybra.counts(data, count_by = 'author') ## counts distinct authors in data.``
        ``hybra.counts(data, count_by = 'domain') ## counts distinct domain in data.``
    """

    try:
        counts_helper = getattr( helpers, 'counts_' + count_by )

        counts_helper( data )

    except Exception, e:
        print(repr(e))
        print("Getting counts failed. Supported features to count by:")

        for c in filter( lambda x: x.startswith('counts_'), dir( helpers ) ):
            print( c.replace('counts_', '') )
