# coding=UTF8

import os, sys

sys.path.append('../core/')

import hybra
import datetime

from helpers import filters
from helpers import counters
from helpers import domains

class TestUM:

    def setup(self):
        self.dataMedia = hybra.data( 'news', data_folder = '', terms = ['yle.json'] )
        self.dataFacebook = hybra.data( 'facebook', data_folder = '', terms = ['facebook.json'] )

    def test_filter_text( self ):
        pass
