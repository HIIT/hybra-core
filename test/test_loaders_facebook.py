import pytest

from hybra import core

class TestUM:

    def setup(self):
        self.data = core.data( 'facebook', folder = '', terms = ['facebook.json'] )
        self.listdata = list( self.data )

    def test_get_everything(self):
        assert len( self.listdata ) == 4

    def test_links(self):
        assert len( self.listdata[0]['links'] ) == 4

        for i, j in enumerate( "http://www.google.com/,http://www.google.com,http://www.hs.fi,http://www.hiit.fi".split(',') ):
            assert self.listdata[0]['links'][ i ] == j

        ## post with no links should be explicit
        assert len( self.listdata[1]['links'] ) == 0

    def test_texts(self):

        texts = ["This is a post with a link http://www.google.com http://www.hs.fi http://www.hiit.fi",
        "Post without comments",
        "Post"]

        for i, j in enumerate( texts ):
            assert self.listdata[i]['text_content'] == j

    def test_dates(self):

        for entry in self.data:

            assert entry['timestamp'] != None
