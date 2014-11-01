"""Module containg metrics for Network Interfaces. """

from abc import ABCMeta, abstractmethod
from use.sys_util import Metric, SystemUtilities

class NetworkMetrics(object):
    """Abstract base class for Network metrics. All implementations
        (depending on OS) should implement the abstract methods defined here."""

    __metaclass__ = ABCMeta


    def __new__(cls):
        return SystemUtilities.get_metric_obj(cls)

    @abstractmethod
    def get_net_util(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Network Utilisation metrics. """
        return NotImplemented

    @abstractmethod
    def get_net_satur(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Network Saturation metrics. """
        return NotImplemented

    @abstractmethod
    def get_net_errors(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Network Errors metrics."""
        return NotImplemented

@Metric('Linux')
class LinuxNetworkMetrics(NetworkMetrics):
    """Network metrics for Linux Systems are obtained here."""

    def get_net_util(self):
        """ Network utilization for Linux is based on /proc/net/dev.
            Returns a dictionary in the form of :

            'interface':[Rbytes,Tbytes] ."""

        return self._get_net_metric("bytes")

    def get_net_satur(self):
        """Network saturation for Linux is based on /proc/net/dev."""

        return self._get_net_metric("drop")

    def get_net_errors(self):
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

