# coding=UTF8

keyword = 'ja'

import os, sys
from hybra import core

core.set_data_path('./data/')

d = core.data( 'news', folder = '', terms = ['yle.json'] )
sample1 = core.filter_by( d, 'text', text = keyword.split(',') )

d = core.data( 'facebook', folder = '', terms = ['facebook.json'] )
sample2 = core.filter_by( d, 'text', text = keyword.split(',') )

import pickle

pickle.dump( sample1 + sample2, open( keyword + '.pickle', 'w' ) )
