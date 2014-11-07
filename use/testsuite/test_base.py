import unittest

from use.metrics.base import Metrics


class TestBaseMetrics(unittest.TestCase):

    def test_instantiation(self):
        with self.assertRaises(TypeError):
            Metrics()

    def test_metaclass(self):
        class SomeMetrics(Metrics):
            pass
        with self.assertRaises(TypeError):
            SomeMetrics()

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

if __name__ == '__main__':
    unittest.main()
