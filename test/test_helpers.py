# coding=UTF8
import pytest

from hybra import core

import datetime
import os

from helpers import filters
from helpers import counters
from helpers import urls
from helpers import exporter



class TestTextFilter:

    def setup(self):
        self.dataMedia = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = core.data( 'facebook', folder = '', terms = ['facebook.json'] )

    def test_filter_text_empty( self ):

        fb = filters.filter_by_text( self.dataFacebook )
        media = filters.filter_by_text( self.dataMedia )

        assert( len( list(fb) ) == 4 )
        assert( len( list(media) ) == 276 )

    def test_filter_text_uppercase(self):

        fb = filters.filter_by_text( self.dataFacebook, text = ['POST'] )
        media = filters.filter_by_text( self.dataMedia, text = ['ALGORITMI'] )

        assert( len(fb) == 3 )
        assert( len(media) == 1 )

    def test_filter_text_substrings(self):

        fb = filters.filter_by_text( self.dataFacebook, text = ['pos'] )
        media = filters.filter_by_text( self.dataMedia, text = ['algorit'] )

        assert( len(fb) == 3)
        assert( len(media) == 1)

    def test_filter_text_substrings_false(self):

        fb = filters.filter_by_text( self.dataFacebook, text = ['pos'], substrings = False )
        media = filters.filter_by_text( self.dataMedia, text = ['algorit'], substrings = False )

        assert( len(fb) == 0 )
        assert( len(media) == 0)

    def test_filter_text_inclusive(self):

        fb = filters.filter_by_text( self.dataFacebook, text = ['post', 'missing text'] )
        media = filters.filter_by_text( self.dataMedia, text = ['algoritmi', 'missing text'] )

        assert( len(fb) == 0 )
        assert( len(media) == 0)

    def test_filter_text_not_inclusive(self):

        fb = filters.filter_by_text( self.dataFacebook, text = ['post', 'missing text'], inclusive = False )
        media = filters.filter_by_text( self.dataMedia, text = ['algoritmi', 'missing text'], inclusive = False )

        assert( len(fb) == 3 )
        assert( len(media) == 1)



class TestDatetimeFilter:

    def setup(self):
        self.dataMedia = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = core.data( 'facebook', folder = '', terms = ['facebook.json'] )

    def test_filter_datetime_no_dates( self ):

        fb = filters.filter_by_datetime( self.dataFacebook )
        media = filters.filter_by_datetime( self.dataMedia )

        assert( len( list(fb) ) == 4 )
        assert( len( list(media) ) == 276 )

    def test_filter_datetime_after(self):

        fb = filters.filter_by_datetime( self.dataFacebook, after = '2017-1-1' )
        media = filters.filter_by_datetime( self.dataMedia, after = '2017-6-30 21:00:00' )

        assert( len(fb) == 2 )
        assert( len(media) == 4)

    def test_filter_datetime_before(self):

        fb = filters.filter_by_datetime( self.dataFacebook, before = '2017-1-1' )
        media = filters.filter_by_datetime( self.dataMedia, before = '2017-6-30 21:00:00' )

        assert( len(fb) == 2 )
        assert( len(media) == 272 )

    def test_filter_datetime_after_before(self):

        fb = filters.filter_by_datetime( self.dataFacebook, after = '2017-1-3 15:09:23', before = '2017-2-6 19:52:09' )
        media = filters.filter_by_datetime( self.dataMedia, after = '2017-6-30 21:00:04', before = '2017-6-30 23:13:53' )

        assert( len(fb) == 1 )
        assert( len(media) == 3 )



class TestAuthorFilter:

    def setup(self):
        self.dataMedia = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = core.data( 'facebook', folder = '', terms = ['facebook.json'] )

    def test_filter_author_empty( self ):

        fb = filters.filter_by_author( self.dataFacebook )
        media = filters.filter_by_author( self.dataMedia )

        assert( len( list(fb) ) == 4 )
        assert( len( list(media) ) == 276 )

    def test_filter_author_one( self ):

        fb = filters.filter_by_author( self.dataFacebook, authors = ['Matti Nelimarkka'] )
        media = filters.filter_by_author( self.dataMedia, authors = ['Teemu Toivola'] )

        assert( len( fb ) == 4 )
        assert( len(media) == 2 )

    def test_filter_author_two( self ):

        fb = filters.filter_by_author( self.dataFacebook, authors = ['Matti Nelimarkka', 'Heikki Heiskanen'] )
        media = filters.filter_by_author( self.dataMedia, authors = ['Teemu Toivola', 'Heikki Heiskanen'] )

        assert( len( fb ) == 4 )
        assert( len(media) == 3 )

    def test_filter_author_not_found( self ):

        fb = filters.filter_by_author( self.dataFacebook, authors = ['Missing author'] )
        media = filters.filter_by_author( self.dataMedia, authors = ['Missing author', 'Missing author2'] )

        assert( len( fb ) == 0 )
        assert( len(media) == 0 )



class TestDomainFilter:

    def setup(self):
        self.dataMedia = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = core.data( 'facebook', folder = '', terms = ['facebook.json'] )

    def test_filter_domain_empty( self ):

        fb = filters.filter_by_domain( self.dataFacebook )
        media = filters.filter_by_domain( self.dataMedia )

        assert( len( list(fb) ) == 4 )
        assert( len( list(media) ) == 276 )

    def test_filter_domain_one( self ):

        fb = filters.filter_by_domain( self.dataFacebook, domains = ['facebook.com'] )
        media = filters.filter_by_domain( self.dataMedia, domains = ['yle.fi'] )

        assert( len( list(fb) ) == 4 )
        assert( len( list(media) ) == 276 )

    def test_filter_domain_missing( self ):

        fb = filters.filter_by_domain( self.dataFacebook, domains = ['twitter.com'] )
        media = filters.filter_by_domain( self.dataMedia, domains = ['hs.fi'] )

        assert( len( list(fb) ) == 0 )
        assert( len( list(media) ) == 0 )



class TestUrls:

    def setup(self):
        self.dataMedia = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = core.data( 'facebook', folder = '', terms = ['facebook.json'] )

    def test_list_links( self ):

        fb = urls.links( self.dataFacebook )
        media = urls.links( self.dataMedia )

        assert( len(fb) == 4 )
        assert( len(media) == 433 )

    def test_extract_domains( self ):

        fb = urls.domains( self.dataFacebook )
        media = urls.domains( urls.links( self.dataMedia ) )

        assert( len(fb) == 4 )
        assert( len(media) == 433 )



class TestCounter:

    def setup(self):
        self.dataMedia = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = core.data( 'facebook', folder = '', terms = ['facebook.json'] )

    def test_count_authors( self ):

        fb = counters.counts_author( self.dataFacebook, verbose = False )
        media = counters.counts_author( self.dataMedia, verbose = False )

        assert( len( fb.keys() ) == 1 )
        assert( len( media.keys() ) == 140 )

    def test_count_domains( self ):

        fb = counters.counts_domain( self.dataFacebook, verbose = False )
        media = counters.counts_domain( self.dataMedia, verbose = False )

        assert( len( fb.keys() ) == 1 )
        assert( len( media.keys() ) == 1 )



class TestXlsxExporter:

    def setup(self):
        self.dataMedia = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = core.data( 'facebook', folder = '', terms = ['facebook.json'] )

        self.out_fb = 'out_fb'
        self.out_media = 'out_media'

    def test_export_generator_xlsx( self ):

        try:
            exporter.export_csv( self.dataMedia, self.out_media + '.xlsx' )
        except Exception, e:
            pytest.fail( "Exception " + str(e) )

        try:
            exporter.export_csv( self.dataFacebook, self.out_fb + '.xlsx' )
        except Exception, e:
            pytest.fail( "Exception " + str(e) )

        assert( os.path.isfile( self.out_media + '.xlsx' ) )
        assert( os.path.isfile( self.out_fb + '.xlsx' ) )

    def test_export_list_xlsx( self ):

        try:
            exporter.export_csv( list( self.dataMedia ), self.out_media + '.xlsx' )
        except Exception, e:
            pytest.fail( "Exception " + str(e) )

        try:
            exporter.export_csv( list( self.dataFacebook ), self.out_fb + '.xlsx' )
        except Exception, e:
            pytest.fail( "Exception " + str(e) )

        assert( os.path.isfile( self.out_media + '.xlsx' ) )
        assert( os.path.isfile( self.out_fb + '.xlsx' ) )

    def teardown( self ):

        os.remove( self.out_media + '.xlsx' )
        os.remove( self.out_fb + '.xlsx' )


class TestCsvExporter:

    def setup(self):
        self.dataMedia = core.data( 'news', folder = '', terms = ['yle.json'] )
        self.dataFacebook = core.data( 'facebook', folder = '', terms = ['facebook.json'] )

        self.out_fb = 'out_fb'
        self.out_media = 'out_media'

    def test_export_generator_csv( self ):

        try:
            exporter.export_csv( self.dataMedia, self.out_media + '.csv' )
        except Exception, e:
            pytest.fail( "Exception " + str(e) )

        try:
            exporter.export_csv( self.dataFacebook, self.out_fb + '.csv' )
        except Exception, e:
            pytest.fail( "Exception " + str(e) )

        assert( os.path.isfile( self.out_media + '.csv' ) )
        assert( os.path.isfile( self.out_fb + '.csv' ) )

    def test_export_list_csv( self ):

        try:
            exporter.export_csv( list( self.dataMedia ), self.out_media + '.csv' )
        except Exception, e:
            pytest.fail( "Exception " + str(e) )

        try:
            exporter.export_csv( list( self.dataFacebook ), self.out_fb + '.csv' )
        except Exception, e:
            pytest.fail( "Exception " + str(e) )

        assert( os.path.isfile( self.out_media + '.csv' ) )
        assert( os.path.isfile( self.out_fb + '.csv' ) )

    def teardown( self ):

        os.remove( self.out_media + '.csv' )
        os.remove( self.out_fb + '.csv' )
