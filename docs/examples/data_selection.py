# coding=UTF8

keyword = 'ja'

import os, sys
from core import hybra

hybra.set_data_path('./data/')

d = hybra.data( 'news', folder = '', terms = ['yle.json'] )
sample1 = hybra.filter_by( d, 'text', text = keyword.split(',') )

d = hybra.data( 'facebook', folder = '', terms = ['facebook.json'] )
sample2 = hybra.filter_by( d, 'text', text = keyword.split(',') )

import pickle

pickle.dump( sample1 + sample2, open( keyword + '.pickle', 'w' ) )

