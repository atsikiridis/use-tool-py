"""Test module for CPU-related classes of use-tool-py."""

import unittest
from usetool.cpu import CpuMetrics, LinuxCpuMetrics

class CpuTest(unittest.TestCase):
    """Class containing unit tests for CPU classes."""

    def setUp(self):
        self.cpu_metrics = CpuMetrics()

    def test_get_cpu_util(self):
        """Test method for get_cpu_util() method.
           Is the output of the method a valid utilisation figure ?"""
        self.assertTrue(0.0 <= float(self.cpu_metrics.get_cpu_util()) <= 100.0)

    def test_get_cpu_satur(self):
        """Test method for get_cpu_satur() method.
           The output of get_cpu_satur must be a dictionary (3 load average
           values, one number of CPU cores)"""
        cpu_satur = self.cpu_metrics.get_cpu_satur()
        self.assertTrue(isinstance(cpu_satur, dict))

    def test_get_cpu_errors(self):
        #empty
        return NotImplemented

    def test_delta_time(self):
        """This private method computes dt for a second interval.
           The test shows what happens if the user passes
           an invalid second interval."""
        self.assertRaises(ValueError, lambda:  LinuxCpuMetrics._delta_time(-100))

    def test_get_time_list(self):
        """This private method reads Cpu data from /proc/stat and returns an object. """
        self.assertTrue(LinuxCpuMetrics._get_time_list())

if __name__ == '__main__':
    unittest.main()
