"""Test Module for StorageIO-related classes of use-tool-ly."""

import unittest
from usetool.storcap import StorageCapMetrics

class MemTest(unittest.TestCase):
    """Class containing unit tests for StorageIO classes."""

    def setUp(self):
        self.storcap_metrics = StorageCapMetrics() 

    def test_get_mem_util(self):
        """Test method for get_mem_util() method.
           Is the output of the method a valid utilisation figure?"""
        self.assertTrue(0.0 <= 
                        float(self.storcap_metrics.get_storcap_util()) <= 100.0)

if __name__ == '__main__':
    unittest.main()
