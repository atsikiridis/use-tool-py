from abc import ABCMeta, abstractproperty
import platform
import inspect

system_map = dict()


class metric(object):

    def __init__(self, system):
        print self, system
        self._system = system

    def __call__(self, *args, **kwargs):
        #print 'call', self, args, kwargs
        # TODO we need to get the first abstract class
        system_map[self._system] = args[0]
        return self

class Metrics(object):

    __metaclass__ = ABCMeta

    def __new__(cls, *args, **kwargs):
        if cls == Metrics or not inspect.isabstract(cls):
            return object.__new__(cls, *args, **kwargs)
        return system_map[platform.system()]()

    @abstractproperty
    def utilization(self):
        return

    @abstractproperty
    def saturation(self):
        return

    @abstractproperty
    def errors(self):
        return


class CpuMetrics(Metrics):

    @abstractproperty
    def utilization_per_core(self):
        pass


class NetworkMetrics(Metrics):

    @abstractproperty
    def utilization_per_nic(self):
        return

MemoryMetrics = Metrics
StorageIOMetrics = Metrics
