# coding=UTF8
import pytest

from core import hybra

import datetime

from helpers import filters
from helpers import counters
from helpers import domains

class TestUM:

    def setup(self):
        self.dataMedia = hybra.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = hybra.data( 'facebook', folder = '', terms = ['facebook.json'] )

        self.dataFacebook = map( lambda x: x, self.dataFacebook )
        self.dataMedia = map( lambda x: x, self.dataMedia )

    def test_filter_text( self ):

        fb = hybra.filter_by( self.dataFacebook, 'text', text = [''] )
        media = hybra.filter_by( self.dataMedia, 'text', text = [''] )

        assert( len(fb) == len(self.dataFacebook) )
        assert( len(media) == len(self.dataMedia) )

        fb = hybra.filter_by( self.dataFacebook, 'text', text = ['Post'] )
        media = hybra.filter_by( self.dataMedia, 'text', text = ['Algoritmi'] )

        assert( len(fb) == 3 )
        assert( len(media) == 1 )

        fb = hybra.filter_by( self.dataFacebook, 'text', text = ['pos'] )
        media = hybra.filter_by( self.dataMedia, 'text', text = ['algorit'] )

        assert( len(fb) == 3)
        assert( len(media) == 1)

        fb = hybra.filter_by( self.dataFacebook, 'text', text = ['pos'], substrings = False )
        media = hybra.filter_by( self.dataMedia, 'text', text = ['algorit'], substrings = False )

        assert( len(fb) == 0 )
        assert( len(media) == 0)

        fb = hybra.filter_by( self.dataFacebook, 'text', text = ['post', 'missing text'] )
        media = hybra.filter_by( self.dataMedia, 'text', text = ['algoritmi', 'missing text'] )

        assert( len(fb) == 0 )
        assert( len(media) == 0)

        fb = hybra.filter_by( self.dataFacebook, 'text', text = ['post', 'missing text'], inclusive = False )
        media = hybra.filter_by( self.dataMedia, 'text', text = ['algoritmi', 'missing text'], inclusive = False )

        assert( len(fb) == 3 )
        assert( len(media) == 1)

    def test_filter_datetime( self ):
        pass

    def test_filter_authors( self ):
        pass

    def test_filter_domain( self ):
        pass

    def test_extract_domains( self ):
        pass

    def test_count_authors( self ):
        pass

    def test_count_domains( self ):
        pass
