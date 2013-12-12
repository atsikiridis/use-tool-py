"""Test Module for Memory-related classes of use-tool-ly."""

import unittest
from usetool.net import NetworkMetrics, LinuxNetworkMetrics

class NetworkTest(unittest.TestCase):
    """Class containing unit tests for Memory classes."""

    def setUp(self):
        self.network_metrics = NetworkMetrics()

    def test_get_net_util(self):
        """Test method for get_net_util() method."""
        net_util = self.network_metrics.get_net_util()
        for value1, value2 in net_util.values():
            self.assertTrue(value1.isdigit())
            self.assertTrue(value2.isdigit())

    def test_get_net_satur(self):
        """Test method for get_cpu_satur() method.
           The output of get_cpu_satur must be a dictionary with
           numerical values"""
        net_satur = self.network_metrics.get_net_satur()
        for value1, value2 in net_satur.values():
            self.assertTrue(value1.isdigit())
            self.assertTrue(value2.isdigit())

    def test_get_net_errors(self):
        """Test method for get_cpu_errors() method.
           A list of two dictionaries wtih numerical values is expected."""
        net_errs = self.network_metrics.get_net_errors()
        for current in net_errs:
            for value1, value2 in current.values():
                self.assertTrue(value1.isdigit())
                self.assertTrue(value2.isdigit())

    def test_get_metric_priv(self):
        """Testing the private method of the Linux Implementation that get
           a column name and returns the appropriate RX/TX values."""
        self.assertRaises(ValueError,
                          lambda: LinuxNetworkMetrics._get_net_metric("foo"))

if __name__ == '__main__':
    unittest.main()
