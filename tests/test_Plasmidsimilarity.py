#!/usr/bin/env python

"""Tests for `Plasmidsimilarity` package."""

import unittest
import pytest
from Plasmidsimilarity.scripts.describe import nucl_count


class TestPlasmidsimilarity(unittest.TestCase):
    """Tests for `Plasmidsimilarity` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.plasmidseq = "ACGTACGTACGTACGT"
        self.plasmidseqwithN = "ACTGNNNN"
    def tearDown(self):
        """Tear down test fixtures, if any."""


    def test_describe(self):
        """Test something."""
        # describe.py test
        assert nucl_count(self.plasmidseq)['A'] == 4
        assert nucl_count(self.plasmidseq)['C'] == 4
        assert nucl_count(self.plasmidseq)['G'] == 4
        assert nucl_count(self.plasmidseq)['T'] == 4
        assert nucl_count(self.plasmidseq)['N'] == 0
        assert nucl_count(self.plasmidseqwithN)['N'] == 4
