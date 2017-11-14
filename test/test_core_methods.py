# coding=UTF8
import pytest

from hybra import core

class TestUM:

    def setup(self):
        self.g = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.l = list( core.data( 'news', folder = '', terms = ['yle.json'] ) )

    def test_describe_generator( self ):
        try:
            core.describe( self.g )
        except Exception, e:
            pytest.fail("Exception " + str(e) )

    def test_describe_list( self ):
        try:
            core.describe( self.l )
        except Exception, e:
            pytest.fail("Exception " + str(e) )

    def test_timeline_generator( self ):
        try:
            core.timeline( datasets = [self.g] )
        except Exception, e:
            pytest.fail("Exception " + str(e) )

    def test_timeline_list( self ):
        try:
            core.timeline( datasets = [self.l] )
        except Exception, e:
            pytest.fail("Exception " + str(e) )

    #def test_wordcloud_generator( self ):
    #    try:
    #        core.wordcloud( data = [self.g] )
    #    except Exception, e:
    #        pytest.fail("Exception " + str(e) )

    #def test_wordcloud_list( self ):
    #    try:
    #        core.wordcloud( data = [self.l] )
    #    except Exception, e:
    #        pytest.fail("Exception " + str(e) )
