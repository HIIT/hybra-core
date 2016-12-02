import data_loader
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from collections import Counter
import re
from matplotlib import pyplot as plt

def create_wordcloud( data ):
    if len(data) == 0:
        print "Dataset empty."
        return

    words = get_words( data )
    frequencies = word_frequencies( words )
    print_frequencies( frequencies )
    frequency_tuples = create_frequency_tuples( frequencies )

    wordcloud = WordCloud( background_color = "white" ).generate_from_frequencies( frequency_tuples )

    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")

def get_words( data ):
    words = []
    for d in data:
        if 'message' in d:
            words += re.findall(r'\w+', d['message'].lower(), re.UNICODE)
    return words

def word_frequencies( word_list ):
    frequencies = Counter( word_list )

    stopwords = ["the", "a", "or", "tai", "and", "ja", "to", "on", "in", "of", "for", "is", "i", "this", "http", "www", "fi", "com"]
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

if __name__ == '__main__':
    data = data_loader.load_facebook()
    create_wordcloud( data )
    plt.show()
