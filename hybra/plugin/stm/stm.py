import requests
import re
import os
import os.path
import pickle

import helpers.urls as urls
import core

from ipywidgets import IntProgress
from IPython.display import display, HTML

MY_DIR = os.path.dirname(os.path.realpath(__file__))

default_stopwords = open( MY_DIR + '/stop_generic_en.txt').readlines() + open( MY_DIR + '/stop_generic.txt').readlines()

def main( data, saveto, k, lasserver = "http://localhost:19990", stopwords = default_stopwords ):

    if len( data ) == 0:
        raise Exception("No data given for analysis.")

    ## data.temp is a temporary file where outcomes of lemmatization is stored in the case that LAS chrashes
    ## check that data is not already lemmatized or that we are not in partial save mode
    if 'text_lemma' not in data[0].keys() or os.path.isfile( saveto + '/data.temp' ):

        display( HTML("<h4>Data preparation</h4>") )

        bar = IntProgress(description='Lemma', min=0, max=len(data) ) # instantiate the bar
        display(bar)

        ## sometimes LAS crashes. This is the temporary file produced in that case of everything done that far.
        if os.path.isfile( saveto + '/data.temp' ):
            display( HTML("<p style='color:grey;'>Temporary file found. Continuing.</p>") )
            data = pickle.load( open(saveto + '/data.temp') )

        ## move URLs
        for entry in data:
            if not 'text_lemma' in entry: ## check this has not been lemmatized before

                entry['text_lemma'] = re.sub( urls.URL_REGEXP, ' ', entry['text_content'] ).strip()

                if len( entry['text_lemma'] ) > 0:
                    try:
                        r = None
                        r = requests.post( lasserver + '/las/baseform', {'text' : entry['text_lemma'] } )
                        r = r.json()

                        entry['text_lemma']  = r['baseform'] or ''
                    except:
                        ## store what we have
                        pickle.dump( data, open(saveto + '/data.temp', 'w' ) ) ## save process this far
                        if r is None:
                            raise Exception("LAS failed: Is LAS server running?")
                        raise Exception("LAS failed: " + str(r) )

            bar.value += 1

        ## TODO: is other kind of preprocessing needed?

        pickle.dump( data, open(saveto + '/data.pickle', 'w' ) )
        os.remove( saveto + '/data.temp' ) ## temporary file not needed anymore, remove it

    documents = map( lambda x: x['text_lemma'], data )
    timestamps = map( lambda x: str( x['timestamp'] ) , data )

    display( HTML("<h4>Data analysis</h4>") )

    stopwords = map( lambda x: x.strip().lower(), stopwords )

    display( HTML("<p>This may take a while</p>") )
    ## this stage does not yet work
    core.plugin( MY_DIR + '/stm.r', documents = documents, timestamps = timestamps, k = k, saveto = saveto, stopwords = stopwords )
