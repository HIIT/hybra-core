# -*- coding: utf-8 -*-

import sys, os
sys.path.append( os.path.dirname(os.path.realpath(__file__) ) )

import os
import random
import types

from loaders import common as datacommon
import importlib

MY_DIR = os.path.dirname(os.path.realpath(__file__))
MY_DIR = MY_DIR.replace('core.', '') ## XXX: hack, should be fixed
DATA_DIR = './data/' ## by default the data comes here

## toggle to check if running in iPYTHON notebook
IPYTHON_NOTEBOOK = False
try:
    get_ipython
    IPYTHON_NOTEBOOK = True
except:
    pass

if IPYTHON_NOTEBOOK:
    from IPython.core.display import HTML, display
    display( HTML('<p><script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.js"></script>Visualisations enabled.</p>') )

def set_data_path( path ):
    """ Sets the path where the data is stored. Relative to where you run your Python.
        :param path: Where the data is stored.
        :type path: str

        :Example:

        * ``core.set_data_path('.') ## search for data from the current folder.``
        * ``core.set_data_path('~/Documents/data/hybra-data') ## data in folder Documents/data/hybra-data.``
    """
    global DATA_DIR
    DATA_DIR = path

    ## when data path is set, automatically print out the versions
    for folder in os.listdir( path ):
        if( os.path.isdir( path + folder ) ):
            datacommon._version( folder )

    return None

def data_path():
    """ Returns the existing data path.
    """
    global DATA_DIR
    return DATA_DIR

def data_sources():
    """ Lists possible data sources hybra core can parse.
    """
    global MY_DIR
    return map( lambda x: x.replace('.py', ''), filter( lambda x: not x.startswith('_') and x.endswith('.py'), os.listdir( MY_DIR + '/loaders/') ) )

def data( source, folder = '', **kwargs ):
    """ Load data of type `source` using the parser for that data.

        :param source: Type of data loaded. Can be `facebook`, `media`, `twitter`.
        :type source: str
        :param folder: Folder under data path that contains the data to be loaded.
        :type folder: str

        :Kwargs:
            * *terms* (*list*) --
              If source is `facebook`, `news` or `twitter`. Terms to be searched for in data filenames. Given as strings.
            * *data_dir* (*str*) --
              Data directory to override set data path.

        :Example:

        ``core.data('news', terms = ['uutiset'], folder = 'yle') ## load news data from files with filename containing the term 'uutiset' from the subfolder YLE in your data folder.``
    """
    global DATA_DIR

    if source not in data_sources():
        raise NameError('Unknown media type')

    loader = importlib.import_module( 'loaders.' + source )

    kwargs['folder'] = folder

    if 'data_dir' not in kwargs:
        kwargs['data_dir'] = DATA_DIR

    return loader.load( **kwargs )

def describe( data ):
    """ Describe the dataset `data`, showing the amount of posts,
        number of authors, historical data and more detailed data sources.

        :param data: Data entries. Given as generator or list.
        :type data: generator or list
    """

    import descriptives
    from IPython.core.display import display, HTML

    return display( HTML( descriptives.describe( data ) ) )

def timeline( datasets = [], **kwargs ):
    """ Draws a timeline the dataset `data`.

        :param datasets: Datasets to plot. Given as generators or lists.
        :type datasets: list

        :Kwargs:
            * *colors* (*list*) --
              List of css colors given as strings to be used in drawing the timeline plots.

        :Example:

        ``core.timeline(datasets[news_data, fb_data], colors = ['blue', 'red']) ## Plots the dataset `news_data` as blue timeline and the dataset `fb_data` as red timeline.``
    """

    from timeline import module_timeline
    from IPython.core.display import display, HTML

    kwargs['datasets'] = datasets

    return display( HTML( module_timeline.create_timeline( **kwargs ) ) )

def network( data ):
    """ Draws a network the dataset `data`.

        :param data: Data entries.
        :type data: generator or list
    """

    from network import module_network
    from IPython.core.display import display, HTML

    return display( HTML( module_network.create_network( data ) ) )

def wordcloud( data, **kwargs ):
    """ Draws a wordcloud the dataset `data`.

        :param data: Data entries.
        :type data: generator or list

        :Kwargs:
            * *stopwords* (*list*) --
              Words to be ignored in generating the wordcloud. Given as strings.
    """

    import wordclouds as module_wordclouds

    module_wordclouds.create_wordcloud( data, **kwargs )

def analyse( script, **kwargs ):
    """ Run R code given in parameter `script` using rpy2.
        You can provide the R code python variables in kwargs and those are automatically transfered to suitable R format.

        :param script: R code or a path to script to be run.
        :type script: str

        :Kwargs:
            Parameters and their values with which to parameterize the R script.

        :Example:

        ``core.analyse( \"\"\"t <- table( df$a, df$b)
        print( chisq.test( t ) )
        \"\"\", df = data)
        ## Runs the χ²-test to examine the expected cross-tabulated frequencies of a and b to observed frequeincies in data. data is a list of dictonaries, each dictonary having a and b variables.``
    """

    from analysis.runr import runr

    globalenv = None
    if 'previous' in kwargs:
        globalenv = kwargs[ g ]
        del kwargs['previous']

    return runr( script, globalenv, **kwargs )

def export( data, file_path ):
    """ Export the dataset `data` in common format to the given file format.
        Recognizes output format from file extension in given file path.
        Accepted formats: .csv, .xlsx

        :param data: Data entries to be exported.
        :type data: generator or list
        :param file_path: Path to output file.
        :type file_path: str

        :Example:

        ``core.export(data, 'exported_data.csv') ## Exports data in common format to file 'exported_data.csv' in current path.``
    """

    from helpers import exporter

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
        Exports the sample to file using the core module export method
        if the parameter `export_file` is not None.

        :param data: Data entries to be sampled.
        :type data: generator or list
        :param size: An integer value specifying the sample size.
        :type size: int
        :param seed: Seed to use in randomization. Defaults to 100.
        :type seed: int
        :param export_file: Path to output file. Defaults to None.
        :type export_file: None or str

        :Example:

        ``core.sample(data, 100, seed = 0, export_file = 'exported_sample.csv') ## Takes a random sample of dataset `data` using the seed 0 and exports it to file 'exported_sample.csv' in current path.``
    """

    if isinstance( data, types.GeneratorType ):
        data = list( data )

    random.seed(seed)

    data_sample = random.sample(data, size)

    if export_file:
        export( data_sample, export_file )

    return data_sample

def filter_by( data, filter_type, **kwargs ):
    """ Filters the dataset `data` with the filter given in `filter_type`.
        Returns the filtered data if `filter_type` matches a filtering method
        in the modude filters.

        :param data: Data entries to be filtered.
        :type data: generator or list
        :param filter_type: Filter type to be used. Can be `text`, `datetime`, `author` or `domain`.
        :type filter_type: str

        :Kwargs:
            * *text* (*list*) --
              If filter_type is `text`. List of strings to use for filtering.
            * *substrings* (*bool*) --
              If filter_type is `text`. If True, will search substrings in text content for terms given in parameter `text`. Defaults to True.
            * *inclusive* (*bool*) --
              If filter_type is `text`. If True, returns only entries with all terms given in parameter `text`. Defaults to True.
            * *after* (*str*) --
              Date and time after which to return entries.
            * *before* (*str*) --
              Date and time before which to return entries.
            * *authors* (*list*) --
              If filter_type is `author`. List of authors as strings to filter by.
            * *domains* (*list*) --
              If filter_type is `domain`. List of domains as strings to filter by.

        :Example:

        * ``core.filter_by(data, 'text', text = ['research']) ## Return from dataset `data` entries which include the term 'research' in text content.``
        * ``core.filter_by(data, 'text', text = ['research', 'science'], substrings = False, inclusive = False) ## Return from dataset `data` entries which include the term 'research' or the term 'science' in text content as full strings.``
        * ``core.filter_by(data, 'datetime', after = '2015-2-15') ## Return from dataset `data` entries with timestamp after the date '2015-2-15'.``
        * ``core.filter_by(data, 'datetime', after = '2017-1-1', before = '2017-6-30 18:00:00') ## Return from dataset `data` entries with timestamp after the date '2017-1-1' and before the time '2017-6-30 18:00:00'.``
        * ``core.filter_by(data, 'author', authors = ['author1', 'author2']) ## Return from dataset `data` entries which have 'author1' or 'author2' as creator.``
        * ``core.filter_by(data, 'domain', domains = ['domain1.com', 'domain2.net']) ## Return from dataset `data` entries which are from domains 'domain1.com' or 'domain2.net'.``
    """

    from helpers import filters

    try:
        filter_helper = getattr( filters, 'filter_by_' + filter_type )

        return filter_helper( data, **kwargs )

    except Exception, e:
        print(repr(e))
        print('Data filtering failed. Supported filters:')

        for f in filter(lambda x: x.startswith('filter_by_'), dir(filters) ):
            print( f.replace('filter_by_', '') )

def counts( data, count_by, verbose = False ):
    """ Counts the occurrences of the feature `count_by` in the dataset `data`.
        Returns the counts as a Counter object and prints them if `verbose` is True.

        :param data: Data entries to be counted.
        :type data: generator or list
        :param count_by: The feature to be used for counting. Can be `author` or `domain`.
        :type count_by: str
        :param verbose: If True, prints the counts. Defaults to False.
        :type verbose: bool

        :Example:

        * ``core.counts(data, count_by = 'author') ## counts distinct authors in data.``
        * ``core.counts(data, count_by = 'domain', verbose = True) ## counts distinct domains in data and print the counts.``
    """

    from helpers import counters

    try:
        counts_helper = getattr( counters, 'counts_' + count_by )

        return counts_helper( data, verbose )

    except Exception, e:
        print(repr(e))
        print("Getting counts failed. Supported features to count by:")

        for c in filter( lambda x: x.startswith('counts_'), dir( counters ) ):
            print( c.replace('counts_', '') )
