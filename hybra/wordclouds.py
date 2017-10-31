from __future__ import absolute_import, division, print_function, unicode_literals

from collections import Counter
import re

def create_wordcloud( data, stopwords = ["the", "a", "or", "tai", "and", "ja", "to", "on", "in", "of", "for", "is", "i", "this", "http", "www", "fi", "com"] ):

    import types

    if isinstance( data, types.GeneratorType ):
        data = list( data )

    if len(data) == 0:
        print( "Dataset empty." )
        return

    from wordcloud import WordCloud
    from matplotlib import pyplot as plt

    words = get_words( data )

    frequencies = Counter( words )

    ## remove stopwords
    for word in stopwords:
        del frequencies[word]

    print_frequencies( frequencies )

    wordcloud = WordCloud( background_color = "white" ).generate_from_frequencies( frequencies.items() )

    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")

def get_words( data ):
    words = []
    for d in data:
        words += re.findall(r'\w+', decode_utf8( d['text_content'].lower() ), re.UNICODE)

        if '_comments' in d:
            for c in d['_comments']:
                if 'message' in c:
                    words += re.findall(r'\w+', decode_utf8( c['message'].lower() ), re.UNICODE)
    return words

def print_frequencies( frequencies ):
    print(  "\nDistinct words:", len(frequencies) )
    print( "10 most common words:" )

    i = 1
    for word in frequencies.most_common(10):
        print( i , " ", word[0], "-", word[1] )
        i += 1


def decode_utf8( string ):
    try:
        return string.decode('utf8')
    except UnicodeEncodeError:
        return string

if __name__ == '__main__':

    from matplotlib import pyplot as plt

    for function_name in dir( data_loader ):

        if 'load_' in function_name:

            print( function_name )
            f =  getattr( data_loader, function_name )
            data = f()
            create_wordcloud( data )
            plt.show()
