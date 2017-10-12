from core import hybra

hybra.set_data_path('./data/')

data = hybra.data( 'news', folder = '', terms = ['yle.json'] )

authors = hybra.counts( data, 'author' )
topauthors = authors.most_common(10)

for name, number in topauthors:
    print "%s (%s)" % (name, number)
