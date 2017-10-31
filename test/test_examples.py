# coding=UTF8
import pytest

import os

from hybra import core

class TestUM:

    def setup(self):
        self.path = './docs/examples/'
        self.files = filter( lambda x: x.endswith('.py'), os.listdir( self.path ) )



    def test_all( self ):

        for f in self.files:

            f = self.path + f

            try:
                execfile( f )
            except Exception, e:
                pytest.fail("Exception " + f + ' ' + str(e) )
