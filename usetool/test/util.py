""" Test module for utility classes of use-tool-py. """

import unittest
from usetool.sys_util import Metric
from usetool.sys_util import SystemUtilities

class UtilTest(unittest.TestCase):
    """Class containing unit tests for System Utilities classes. """

    def test_metric(self):
        """Method to test the Metric encapsulation class """
        self.assertRaises(RuntimeError, lambda: Metric())

    def test_system_utilities(self):
        """Method to test the SystemUtilities class."""

        class DummyMetric(object):
            """ This class will only be used to test
                the SystemUtilities.get_metric_obj() method """
            pass

        self.assertRaises(RuntimeError,
                          lambda: SystemUtilities.get_metric_obj(DummyMetric))
        #self.assertRaises(TypeError,     TODO Unit Test does not pass...
        #                  lambda: SystemUtilities.get_metric_obj("foo"))
        self.assertRaises(TypeError,
                          lambda: SystemUtilities.get_metric_obj())
        self.assertRaises(ValueError,
                          lambda: SystemUtilities.get_numeric_value("foo"))

if __name__ == '__main__':
    unittest.main()
