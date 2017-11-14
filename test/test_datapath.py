# coding=UTF8
import pytest

from hybra import core

class TestUM:

    def setup(self):

        core.set_data_path('./data_empty/')

    def test_is_changed( self ):
        assert( core.data_path() == './data_empty/' )
