from __future__ import print_function
from hybra import core

core.set_data_path('./data/')

yle = core.data( 'news', folder = '', terms = ['yle.json'] )

yle_cats = core.filter_by( yle, 'text', text = ['kissa'] )

print(len( yle_cats ))
