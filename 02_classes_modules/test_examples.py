#!/usr/bin/env python

import doctest
import unittest
import glob

suite = unittest.TestSuite()

for file_name in glob.glob('*.pycon'):
    suite.addTest(doctest.DocFileSuite(file_name))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
