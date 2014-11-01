"""Module containing metrics relevant to Storage Capacity."""

from abc import ABCMeta, abstractmethod
from use.sys_util import Metric, SystemUtilities

class StorageCapMetrics(object):
    """Abstract base class for Storage capacity metrics. All implementations
      (depending on OS) should implement the abstract methods defined here."""

    __metaclass__ = ABCMeta

    def __new__(cls):
        return SystemUtilities.get_metric_obj(cls)

    @abstractmethod
    def get_storcap_util(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Storage Capacity Utilisation metrics. """
        return NotImplemented

    @abstractmethod
    def get_storcap_satur(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Storage Capacity Saturation metrics. """
        return NotImplemented

@Metric('Linux')
class LinuxStorageCapMetrics(StorageCapMetrics):
    """Memory metrics for Linux Systems are obtained here."""

    def get_storcap_util(self):
        """Storage capacity utilization in Linux is based on /proc/meminfo.
           Total Swap and Free swap are used. If no swap is used,
           0 is returned."""

        with open("/proc/meminfo") as meminfo_file:
            totalswapindex = 13 #No of line containing the Total Swap metric.
            freeswapindex = 14 #No of line containing the Free Swap metric.
            for index, current in enumerate(meminfo_file):
                if index == totalswapindex:
                    totalswap = current.split(":")[1] #Not Numeric.
                    totalswap = SystemUtilities.get_numeric_value(totalswap)
                elif index == freeswapindex:
                    freeswap = current.split(":")[1] #Not Numeric.
                    freeswap = SystemUtilities.get_numeric_value(freeswap)
        try:
            return str((1 - freeswap / totalswap) * 100)
        except ZeroDivisionError: # If no swapping, totalSwap is zero.
            return 0

    def get_storcap_satur(self):
        return NotImplemented

    def get_storcap_errors(self):
        return NotImplemented
