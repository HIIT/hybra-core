import os
import time
from string import Template

from IPython.core.display import HTML, display

from collections import Counter

path = os.path.dirname(os.path.abspath(__file__))

def create_wordcloud( data, plt, stopwords = ["the", "a", "or", "tai", "and", "ja", "to", "on", "in", "of", "for", "is", "i", "this", "http", "www", "fi", "com"] ):

    import codecs
    html_template = Template( codecs.open( path + '/wordcloud.html', 'r').read() )
    js_template = Template(codecs.open(path + '/wordcloud.js', 'r').read())
    css_text = codecs.open(path + '/wordcloud.css', 'r').read()

    texts = ""
    for node in data:
        text = node['text_content']
        text = text.replace(",", "")
        text = text.replace(".", "")
        text = text.replace("!", "")
        text = text.replace("?", "")
        for word in text.split(" "):
            if word not in stopwords:
                texts += word + " "

    frequencies = Counter(texts.split())
    freqs_list = []
    for key, value in frequencies.iteritems():
        freqs_list.append({"text":encode_utf8(key),"size":str(value)})

    graph_div_id = int(time.time() * 1000)
    js_text = js_template.substitute({'frequencies': str(freqs_list), 'graph_div_id': graph_div_id})
    html_template = html_template.substitute({'js': js_text, 'graph_div_id': graph_div_id, 'css': css_text})

    display( HTML( html_template ) )

    return None

def encode_utf8( string ):
    try:
        return string.encode('utf8')
    except UnicodeDecodeError:
        return string