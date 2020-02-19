from __future__ import print_function
from hybra import core

core.set_data_path('./data/')

data = core.data( 'news', folder = '', terms = ['yle.json'] )

authors = core.counts( data, 'author' )
topauthors = authors.most_common(10)

for name, number in topauthors:
    print("%s (%s)" % (name, number))
