import data_loader
import descriptives
import network
import timeline
import wordclouds


def load_data( terms = [], data_folder = '' ):
    if data_folder == '':
        return load_all_data( terms )
    else:
        if '/' not in data_folder:
            data_folder += '/'
        loader = data_folder.split( '/' )[0]
        return load_data_from_folder( terms, loader, data_folder )


def load_all_data( terms ):
    data = {}

    for function_name in dir( data_loader ):
        if 'load_' in function_name:
            if len( terms ) == 0:
                f =  getattr( data_loader, function_name )
            else:
                f = getattr( data_loader, function_name )( *terms )
            data[function_name] = f()

    return data

def load_data_from_folder( terms, loader, data_folder ):
    data = []

    for function_name in dir( data_loader ):
        if loader in function_name:
            if len( terms ) == 0:
                data += getattr( data_loader, function_name )( data_folder = data_folder )
            else:
                data += getattr( data_loader, function_name)( terms, data_folder )

    return data

def describe( data ):
    if isinstance( data, dict ):
        for loader in data:
            print loader
            descriptives.describe( data[loader] )
            print '\n'
    else:
        descriptives.describe( data )

def create_timeline( data ):
    timeline.create_timeline( data )

def create_network( data ):
    network.create_network( data )

def create_wordcloud( data ):
    wordclouds.create_wordcloud( data )
