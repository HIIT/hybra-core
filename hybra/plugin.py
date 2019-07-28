import os

## for python code
import importlib

## for r-code
import pandas
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import default_converter
from rpy2.robjects import pandas2ri
## convert magic
from rpy2.robjects.conversion import Converter
import types

pandas2ri.activate()

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
        return pandas2ri.py2rpy( dataframe )

    ## default to NA just in case
    return rpy2.rinterface.NA_Real

simple_conver = Converter('simple')
simple_conver.py2rpy.register( list, list_to_vector )
simple_conver.py2rpy.register( types.GeneratorType, list_to_vector )

converter = default_converter + simple_conver

def run( execute, globalenv = None, **kwargs ):

    ## search inside analysis folder
    home = os.path.realpath(__file__)

    ## check if the command is a python file

    f = os.path.dirname( home ) + '/' + execute + '.py'

    if os.path.isfile( f ):
        execute = f


    if os.path.isfile( execute ) and execute.endswith('.py'):
        module = importlib.util.spec_from_file_location( 'main', execute )
        module = importlib.util.module_from_spec( module )
        return module.main( **kwargs )

    ## assume script is R

    if globalenv:
        rpy2.robjects.globalenv = globalenv

    for name, value in kwargs.items():

        ## for debug conversion errors
        # print name
        # print type( value )

        if isinstance( value, dict ):
            ## use pandas
            value = pandas.DataFrame.from_dict( value )
            rpy2.robjects.globalenv[ name ] = pandas2ri.py2rpy( value )
        else:
            rpy2.robjects.globalenv[ name ] = converter.py2rpy( value )

    f = os.path.dirname( home ) + '/' + execute + '.r'

    if os.path.isfile( f ):
        execute = open( f ).read()

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

    run( execute, example1 = [1,2,3,4], example2 = [{'name': 'example2', 'value': 5}]  )
