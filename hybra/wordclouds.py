from __future__ import absolute_import, division, print_function, unicode_literals

from collections import Counter
import re

def create_wordcloud( data, plt, stopwords = ["the", "a", "or", "tai", "and", "ja", "to", "on", "in", "of", "for", "is", "i", "this", "http", "www", "fi", "com"] ):

    import types

    if isinstance( data, types.GeneratorType ):
        data = list( data )

    if len(data) == 0:
        print( "Dataset empty." )
        return

    from wordcloud import WordCloud

    text = ''
    for d in data:
        text += d['text_content'].lower() + ' '
    text = text.strip()

    stopwords = map( lambda w: str(w), stopwords )

    wc = WordCloud( background_color="white", width=800, height=400, stopwords = stopwords )
    wc.generate( text )

    plt.figure(figsize=(15,10))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
