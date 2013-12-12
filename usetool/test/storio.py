"""Test Module for StorageIO-related classes of use-tool-ly."""

import unittest
from usetool.storio import StorageIOMetrics, LinuxStorageMetrics

class StorageIOTest(unittest.TestCase):
    """Class containing unit tests for Memory classes."""

    def setUp(self):
        self.storio_metrics = StorageIOMetrics()

    def test_get_storio_util(self):
        """Test method for get_storio_util() method.
           Is the output of the method a valid utilisation figure?"""
        self.assertTrue(0.0 <=
            float(self.storio_metrics.get_storio_util()) <= 100.0)


    def test_get_storio_satur(self):
        """Test method for get_storio_satur() method.
           The output of get_cpu_satur must be an integer
           as it represents a number of requests."""
        self.assertTrue( self.storio_metrics.get_storio_satur().isdigit() )

    def test_sda_stat_priv(self):
        """Test method for _getsda_stat().
           The output of _getsda_stat() should be a digit.
           Checking corner case, too."""
        self.assertTrue( LinuxStorageMetrics._getsda_stat(5).isdigit() )
        self.assertRaises(IndexError,
                          lambda: LinuxStorageMetrics._getsda_stat(99))

if __name__ == '__main__':
    unittest.main()
