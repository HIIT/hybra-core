from wordcloud import WordCloud
from matplotlib import pyplot as plt
from collections import Counter
import re

def create_wordcloud( data ):
    if len(data) == 0:
        print "Dataset empty."
        return

    text = get_messages( data )
    frequencies = word_frequencies( text )
    print_frequencies( frequencies )
    frequency_tuples = create_frequency_tuples( frequencies )

    wordcloud = WordCloud().generate_from_frequencies( frequency_tuples )

    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")

def get_messages( data ):
    text = ''
    for d in data:
        if 'message' in d:
            text = text + d['message'] + ' '
        for c in d['__comments']:
            if 'message' in c:
                text = text + c['message'] + ' '
    return text.strip()

def word_frequencies( text ):
    text_lower = text.lower()
    words = re.findall(r'\w+', text_lower, re.UNICODE)

    frequencies = Counter( words )

    stopwords = ["the", "a", "or", "tai", "and", "ja"]
    for word in stopwords:
        del frequencies[word]

    return frequencies

def print_frequencies( frequencies ):
    print "\n" + "Distinct words: " + str( len(frequencies) ) + "\n"
    print "10 most common words: "

    i = 1
    for word in frequencies.most_common(10):
        print str( i ) + ". " + word[0] + " - " + str( word[1] )
        i += 1

def create_frequency_tuples( frequencies ):
    tuples = []
    for freq in frequencies:
        tuples.append( (freq, frequencies[freq]) )
    return tuples
