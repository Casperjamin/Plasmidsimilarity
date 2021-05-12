#!/usr/bin/env python

"""Tests for `Plasmidsimilarity` package."""

import unittest
from Plasmidsimilarity.scripts.describe import nucl_count
from Plasmidsimilarity.cli import snakemake_in


class TestPlasmidsimilarity(unittest.TestCase):
    """Tests for `Plasmidsimilarity` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.plasmidseq = "ACGTACGTACGTACGT"
        self.plasmidseqwithN = "ACTGNNNN"
        self.testsequences = [
            "Plasmidsimilarity/testdata/MG800340.1.fasta",
            "Plasmidsimilarity/testdata/MH061380.1.fasta",
            "Plasmidsimilarity/testdata/MK360916.1.fasta",
            "Plasmidsimilarity/testdata/NZ_CP038265.1.fasta",
            "Plasmidsimilarity/testdata/NZ_CP040891.1.fasta"]
        self.snakemake_output = 'testoutput'

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
