#!/usr/bin/env python3
#  coding=utf-8

"""
Tests for the vasp_postprocess package.
"""

# Import package, test suite, and other packages as needed
import os
import unittest
import logging
from lattice_and_bandgap import main
from common import capture_stdout, capture_stderr, diff_lines, silent_remove

__author__ = 'kpgreenm'

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)
DATA_DIR = os.path.join(os.path.dirname(__file__), './data')


class TestExpectedOutput(unittest.TestCase):
    # These will show example usage
    def testStructuralOutput(self):
        try:
            main(['-s'])
            self.assertFalse(diff_lines('unitcell.txt', './tests/unitcell_correct.txt'))
        finally:
            silent_remove('unitcell.txt')

    def testElectronicOutput(self):
        try:
            main(['-e'])
            self.assertFalse(diff_lines('bandgap.txt', './tests/bandgap_correct.txt'))
        finally:
            silent_remove('bandgap.txt')

    def testStructuralAndElectronicOutput(self):
        try:
            main(['-a'])
            self.assertFalse(diff_lines('unitcell.txt', './tests/unitcell_correct.txt'))
            self.assertFalse(diff_lines('bandgap.txt', './tests/bandgap_correct.txt'))
        finally:
            silent_remove('unitcell.txt')
            silent_remove('bandgap.txt')
