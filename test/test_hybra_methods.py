# coding=UTF8

import os, sys
import pytest

sys.path.append('../core/')

import hybra

class TestUM:

    def setup(self):
        self.g = hybra.data( 'news', data_folder = '', terms = ['yle.json'] )
        self.l = list( hybra.data( 'news', data_folder = '', terms = ['yle.json'] ) )

    def test_describe_generator( self ):
        try:
            hybra.describe( self.g )
        except Exception, e:
            pytest.fail("Exception " + str(e) )

    def test_describe_list( self ):
        try:
            hybra.describe( self.l )
        except Exception, e:
            pytest.fail("Exception " + str(e) )

    def test_timeline_generator( self ):
        try:
            hybra.timeline( datasets = [self.g] )
        except Exception, e:
            pytest.fail("Exception " + str(e) )

    def test_timeline_list( self ):
        try:
            hybra.timeline( datasets = [self.l] )
        except Exception, e:
            pytest.fail("Exception " + str(e) )

    #def test_wordcloud_generator( self ):
    #    try:
    #        hybra.wordcloud( data = [self.g] )
    #    except Exception, e:
    #        pytest.fail("Exception " + str(e) )

    #def test_wordcloud_list( self ):
    #    try:
    #        hybra.wordcloud( data = [self.l] )
    #    except Exception, e:
    #        pytest.fail("Exception " + str(e) )
