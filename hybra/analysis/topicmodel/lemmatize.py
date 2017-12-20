# coding: utf-8

import os
import sys
import re
import subprocess

## todo: not sure if smart
sys.path.append('../../')
from helpers import urls as urlshelper

def lemmatize( text, path ):

    try:
        text = text.decode('utf8')
    except:
        return None

    ## remove URLs

    urls = urlshelper.extract( text )

    for url in urls:
        text = text.replace( url, '')

    text = re.sub( u'[^a-zA-ZöäåÖÄÅ\.,:?!;]' , ' ' , text ) ## allow basic välimerkit
    ## Add spaces around all non-alphanumeric characters except _ and -
    text = re.sub( u'([^a-zA-Z0-9_åäöÅÄÖ\-\s])', r' \1 ' , text)
    text = re.sub( ' +',' ', text )
    text = text.replace('"', '' ) ## no "

    try:
        out = subprocess.check_output( 'module load finnish-process; echo "' + text + '" | finnish-process', shell = True)
    except:

        ## In case the above returns an argument too long error, write the command in a shell script and run it
        ## The shell script is written in a file called file_name.sh in the directory that lemmatize.py is ran from
        ## and removed immediately afterwards.

        file_name = path.rsplit('/', 1)[1]

        with open(file_name + '.sh', 'w') as f:
	    cmd = '#!/bin/bash -l\n\nmodule load finnish-process; echo "' + text + '" | finnish-process'
            f.write(cmd.encode('utf-8'))

        os.chmod(file_name + '.sh', 0o777)
        out = subprocess.check_output([os.path.dirname(os.path.realpath(__file__)) + '/' + file_name + '.sh'], shell = False)
        os.remove(file_name + '.sh')

    lemma = ''

    for line in out.split('\n'):
        line = line.strip()
        line = line.split('\t')

        if len( line ) >= 2:
            lemma += line[1] + ' '

    return lemma

## read a file and lemmatize it
def file( path ):

    text = open( path )
    text = text.readlines()
    text = map( lambda x: x.strip(), text )
    text = ' '.join( text )

    lemma = lemmatize( text, path )

    if lemma is None:
        ## Happens if e.g. file only contains urls
        return

    fo = open( path + '.lemma', 'w' )
    fo.write( lemma )
    fo.close()

## read every file in folder and fix based on that
def folder( path ):

    for f in os.listdir( path ):

        file( path + '/' + f )


def serial( path , index ):

   files = os.listdir( path )

   files = filter( lambda x: '.lemma' not in x, files )

   files = filter( lambda x: hash(x) % 200 == index , files )

   for f in files:
       file( path + '/' + f )

if __name__ == '__main__':

    path_arg = 1

    if sys.argv[1] == 'array': ## for running as an array job
        for path in sys.argv[3:]:
            serial( path , int( sys.argv[2] ) )
        path_arg = 3

    else:
        for item in sys.argv[path_arg:]:
            if( os.path.isdir( item ) ):
                folder( item )
            else:
                file( item )
