from abc import ABCMeta, abstractproperty


class Metrics(object):

    __metaclass__ = ABCMeta

    @abstractproperty
    def utilization(self):
        return

    @abstractproperty
    def saturation(self):
        return

    @abstractproperty
    def errors(self):
        return