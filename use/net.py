"""Module containg metrics for Network Interfaces. """

from psutil import net_io_counters

from abc import ABCMeta, abstractproperty
from collections import namedtuple

class NetworkMetrics(object):
    """Abstract base class for Network metrics. All implementations
        (depending on OS) should implement the abstract methods defined here."""

    __metaclass__ = ABCMeta

    @abstractproperty
    def utilization_per_nic(self):
        return

class LinuxNetworkMetrics(NetworkMetrics):
    """Network metrics for Linux Systems are obtained here."""

    def __init__(self):
        self._util_tuple = namedtuple('netutil',
                                         ['bytes_recv', 'bytes_sent'])

    @property
    def utilization(self):
        """ Network utilization for Linux is based on /proc/net/dev.
            Returns a dictionary in the form of :

            'interface':[Rbytes,Tbytes] ."""

        counters = net_io_counters()
        return self._util_tuple(counters.bytes_recv, counters.bytes_sent) # TODO Max bandwidth ?

    @property
    def utilization_per_nic(self):
        all_counters_pernic = net_io_counters(pernic=True)

        counters_per_nic = dict()
        for nic in all_counters_pernic.keys():
            recv_sent = self._util_tuple(all_counters_pernic[nic].bytes_recv,
                                         all_counters_pernic[nic].bytes_sent)
            counters_per_nic[nic] = recv_sent
        return counters_per_nic


    @property
    def saturation(self):
        """Network saturation for Linux is based on /proc/net/dev. drop?"""

        return self._get_net_metric("drop")

    @property
    def errors(self):
        """Network errors for Linux."""
        drop_metric =  LinuxNetworkMetrics._get_net_metric("drop")
        errors_metric =  LinuxNetworkMetrics._get_net_metric("errs")
        return drop_metric, errors_metric

    @classmethod
    def _get_net_metric(cls, column_name):
        """ Since all three metrics are currently being calculated from
            same file, this column returns the appropriate column
            based on column name."""
        metrics_dict = dict()
        with open("/proc/net/dev") as netdevfile:
            for index, current in enumerate(netdevfile):
                if index == 1:
                    #Omits special character of file
                    current = current.replace("|","")
                    headers = current.split()
                    try:
                        no_of_header = headers.index(column_name) - 1
                    except ValueError:
                        raise ValueError(column_name + """ is not a column name
                                                           in /proc/net/dev""")
                elif index >= 2: # First line of data.
                    ifc_info = current.split(": ")

                    # Column before ': ' contains interface name
                    ifc_name = ifc_info[0] # Column before ': '
                    rvalue = ifc_info[1].split()[no_of_header] # RX value
                    tvalue = ifc_info[1].split()[no_of_header + 8] # TX value
                    metrics_dict[ifc_name] = [rvalue, tvalue]
        return metrics_dict

