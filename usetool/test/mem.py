"""Test Module for Memory-related classes of use-tool-ly."""

import unittest
from usetool.mem import MemoryMetrics

class MemTest(unittest.TestCase):
    """Class containing unit tests for Memory classes."""

    def setUp(self):
        self.memory_metrics = MemoryMetrics()

    def test_get_mem_util(self):
        """Test method for get_mem_util() method.
           Is the output of the method a valid utilisation figure?"""
        self.assertTrue(0.0 <=
                        float(self.memory_metrics.get_mem_util()) <= 100.0)

    def test_get_mem_satur(self):
        """Test method for get_cpu_satur() method. Output must be a string."""
        self.assertTrue(  self.memory_metrics.get_mem_satur() )

    def test_get_mem_errors(self):
        """Test method for get_mem_errors() method. """
        self.assertTrue(self.memory_metrics.get_mem_errors() )

if __name__ == '__main__':
    unittest.main()
