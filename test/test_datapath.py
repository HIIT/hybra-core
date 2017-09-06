# coding=UTF8
import pytest

from core import hybra

class TestUM:

    def setup(self):

        hybra.set_data_path('./data2/')
        self.g = hybra.data( 'news', folder = '', terms = ['yle.json'] )

    def test_is_changed( self ):
        assert( hybra.data_path() == './data2/' )
