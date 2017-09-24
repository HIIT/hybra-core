import os

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import default_converter

import pandas
from rpy2.robjects import pandas2ri

## convert magic
from rpy2.robjects.conversion import Converter

import types

simple_conver = Converter('simple')

def list_to_vector( l ):

    if isinstance(l, types.GeneratorType):
        l = list(l)

    if len( l ) == 0:
        return rpy2.rinterface.NA_Real

    if isinstance( l[0], str ):
        return rpy2.rinterface.StrSexpVector( l )
    if isinstance( l[0], int ):
        return rpy2.rinterface.IntSexpVector( l )
    if isinstance( l[0], float ):
        return rpy2.rinterface.FloatSexpVector( l )
    if isinstance( l[0], bool ):
        return rpy2.rinterface.BoolSexpVector( l )

    if isinstance( l[0], dict ): ## need to convert to data frame

        ## let's hope the keys are always the same for each of things in the list
        keys = l[0].keys()

        ## init new dict where values are collected
        dataframe = {}

        for key in keys:
            dataframe[ key ] = []

        for row in l:
            for key in keys:
                if key not in row:
                    value = None
                else:
                    value = row[key]

                dataframe[ key ].append( value )

        dataframe = pandas.DataFrame.from_dict( dataframe )
        return pandas2ri.py2ri( dataframe )


simple_conver.py2ri.register( list, list_to_vector )
simple_conver.py2ri.register( types.GeneratorType, list_to_vector )

converter = default_converter + simple_conver

def runr( execute, globalenv = None, **kwargs ):

    if globalenv:
        rpy2.robjects.globalenv = globalenv

    for name, value in kwargs.items():

        if isinstance( value, dict ):
            ## use pandas
            value = pandas.DataFrame.from_dict( value )
            rpy2.robjects.globalenv[ name ] = pandas2ri.py2ri( value )
        else:
            rpy2.robjects.globalenv[ name ] = converter.py2ri( value )


    ## rpy2.robjects.globalenv['cats'] = interface.p2ri( kwargs['cats'] )

    ## search inside analsis folder
    p = os.path.realpath(__file__)
    p = os.path.dirname( p ) + '/' + execute + '.r'

    if os.path.isfile( p ):
        execute = open( p ).read()

    if os.path.isfile( execute ):
        execute = open( execute ).read()


    robjects.r( execute )

    return robjects.r ## return all computed things

if __name__ == '__main__':
    execute = '''
        library('ggplot2')
        # create a function `f`
        f <- function(r, verbose=FALSE) {
            if (verbose) {
                cat("I am calling f().\n")
            }
            2 * pi * r
        }
        # call the function `f` with argument value 3
        print( f(3) )
        #print( example1 )
        #print( example2 )
        x = f(4)
        '''

    runr( execute, example1 = [1,2,3,4], example2 = [{'name': 'example2', 'value': 5}]  )
