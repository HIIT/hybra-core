#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import time
from string import Template
import random
import re

from IPython.core.display import HTML, display

from collections import Counter

path = os.path.dirname(os.path.abspath(__file__))

def create_wordcloud( data, plt, stopwords = ["the", "a", "or", "tai", "and", "ja", "to", "on", "in", "of", "for", "is", "i", "this", "http", "www", "fi", "com"], width=850, height=350 ):

    import codecs
    html_template = Template( codecs.open( path + '/wordcloud.html', 'r').read() )
    js_template = Template(codecs.open(path + '/wordcloud.js', 'r').read())
    css_text = codecs.open(path + '/wordcloud.css', 'r').read()

    texts = ""
    for node in data:
        text = encode_utf8(node['text_content'])
        text = re.sub('[^0-9a-zA-Zöä\s]+', '', text)
        for word in text.split(" "):
            if word not in stopwords:
                texts += word + " "

    frequencies = Counter(texts.split())
    freqs_list = []
    colors = ["#A5E6BA", "#9AC6C5", "#7785AC", "#248757", "#360568", "#F0544F", "#e07f9f", "#1d7059", "#3e6282"]

    for key, value in frequencies.iteritems():
        freqs_list.append({"text":encode_utf8(key),"size":str(value), "color": random.choice(colors)})

    graph_div_id = int(time.time() * 1000)

    js_text = js_template.substitute({'frequencies': str(freqs_list), 'graph_div_id': graph_div_id, 'width': width, 'height': height})
    html_template = html_template.substitute({'js': js_text, 'graph_div_id': graph_div_id, 'css': css_text})

    display( HTML( html_template ) )

    return None

def encode_utf8( string ):
    try:
        return string.encode('utf8')
    except UnicodeDecodeError:
        return string