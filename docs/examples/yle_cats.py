from core import hybra

hybra.set_data_path('./data/')

yle = hybra.data( 'news', folder = '', terms = ['yle.json'] )

yle_cats = hybra.filter_by( yle, 'text', text = ['kissa'] )

print len( yle_cats )
