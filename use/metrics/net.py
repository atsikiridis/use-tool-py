"""Module containg metrics for Network Interfaces. """
from collections import namedtuple
from abc import ABCMeta, abstractproperty

from use.metrics.base import Metrics

from psutil import net_io_counters


class NetworkMetrics(Metrics):

    __metaclass__ = ABCMeta

    @abstractproperty
    def utilization_per_nic(self):
        return

class LinuxNetworkMetrics(NetworkMetrics):
    """Network metrics for Linux Systems are obtained here."""
    _util_tuple = namedtuple('net_util', ['bytes_recv', 'bytes_sent'])

    @property
    def utilization(self):
        """ Network utilization for Linux is based on /proc/net/dev.
            Returns a dictionary in the form of :

            'interface':[Rbytes,Tbytes] ."""

        counters = net_io_counters()
        return LinuxNetworkMetrics._util_tuple(counters.bytes_recv,
                                               counters.bytes_sent)  # TODO max
                                                                     # ethtool

    @property
    def utilization_per_nic(self):
        all_counters_per_nic = net_io_counters(pernic=True)

        counters_per_nic = dict()
        for nic in all_counters_per_nic.keys():
            received = all_counters_per_nic[nic].bytes_recv
            sent = all_counters_per_nic[nic].bytes_sent
            received_sent = LinuxNetworkMetrics._util_tuple((received, sent))
            counters_per_nic[nic] = received_sent
        return counters_per_nic

    @property
    def saturation(self):
        """Network saturation for Linux is based on /proc/net/dev. drop?"""
        raise NotImplementedError

    @property
    def errors(self):
        """Network errors for Linux. errors i guess?"""
        raise NotImplementedError
