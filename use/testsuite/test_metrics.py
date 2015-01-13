import unittest
import platform
from abc import ABCMeta

from use.metrics import Metrics, metric


class TestMetrics(unittest.TestCase):

    def test_instantiation(self):
        with self.assertRaises(TypeError):
            Metrics()

    def test_metaclass(self):
        class SomeMetrics(Metrics):
            pass
#        with self.assertRaises(TypeError):
#            SomeMetrics()

        class SomeOtherMetrics(Metrics):

            def utilization(self):
                return

            def saturation(self):
                return

            def errors(self):
                return
        try:
            SomeOtherMetrics()
        except TypeError:
            self.fail("""Unexpectedly cannot instantiate a Metric where
                         utilization, saturation, and errors are not abstract
                         properties.""")


class TestSystemDiscovery(unittest.TestCase):

    class ComponentMetrics(Metrics):
        __metaclass__ = ABCMeta

    @metric(platform.system())
    class SystemSpecificComponentMetrics(ComponentMetrics):
        def utilization(self):
            return

        def saturation(self):
            return

        def errors(self):
            return

        @property
        def system(self):
            """Test Method"""
            return platform.system()

    def setUp(self):
        self._metrics = self.ComponentMetrics()

    def test_system_discovery(self):
        self.assertEqual(self._metrics.system, platform.system())

if __name__ == '__main__':
    unittest.main()
