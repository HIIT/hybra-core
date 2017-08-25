# coding=UTF8

import os, sys

import pytest

sys.path.append('../core/')

class TestUM:

    def setup(self):
        self.path = '../docs/examples/'
        self.files = filter( lambda x: x.endswith('.py'), os.listdir( self.path ) )



    def test_all( self ):

        for f in self.files:

            f = self.path + f

            try:
                execfile( f )
            except Exception, e:
                pytest.fail("Exception " + f + ' ' + str(e) )
