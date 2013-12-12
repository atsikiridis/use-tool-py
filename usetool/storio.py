"""Module containing classes for Storage IO-related Metrics."""

from abc import ABCMeta, abstractmethod
from usetool.sys_util import Metric, SystemUtilities
import time

class StorageIOMetrics(object):
    """Abstract base class for Storage IO  metrics. All implementations
        (depending on OS) should implement the abstract methods defined here."""

    __metaclass__ = ABCMeta

    def __new__(cls):
        return SystemUtilities.get_metric_obj(cls)

    @abstractmethod
    def get_storio_util(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Storage IO Utilisation metrics."""
        return NotImplemented

    @abstractmethod
    def get_storio_satur(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Storage IO Saturation metrics. """
        return NotImplemented

    @abstractmethod
    def get_storio_errors(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Storage IO Errors metrics."""
        return NotImplemented

@Metric('Linux')
class LinuxStorageMetrics(StorageIOMetrics):
    """Network metrics for Linux Systems are obtained here."""

    INTERVAL = 2 #delta time

    def get_storio_util(self):
        """ Storage IO utilization in Linux is based on /proc/diskstats.
             or sys/block/sda/stat (Field 10) and /proc/stat.

             util = blkio.ticks / deltams * 100

             blkio.ticks is the tenth field of /sys/block/sda/stat

             deltams = 1000 * ((new_cpu.user + new_cpu.system
                                + new_cpu.idle + new_cpu.iowait) -
                               (old_cpu.user + old_cpu.system
                                + old_cpu.idle + old_cpu.iowait) / ncpu /

             cpu data are from /proc/stat

             util = 100% means that each time the kernel looked,
             an I/O request was in progress."""

        first_millis_io = LinuxStorageMetrics._getsda_stat(9)
        time.sleep(self.INTERVAL)
        second_millis_io = LinuxStorageMetrics._getsda_stat(9)
        util =  float((float(second_millis_io) - float(first_millis_io)) /
                 self.INTERVAL / 10)
        if util > 100: # util can be more than 100 as other devices
                       # may assist handling the load.
            return 100.0
        else:
            return util

    @classmethod
    def _getsda_stat(cls, index):
        """ This private method gets value for the number of
            the column specified."""
        with open("/sys/block/sda/stat") as sdafile:
            try:
                return  sdafile.next().split()[index] #  Millis doing IO
            except IndexError:
                raise IndexError("Invalid column index: " + str(index))


    def get_storio_satur(self):
        """ The wait queue length of the sda is the 9th column in
            /sys/block/sda/stat."""
        return self._getsda_stat(8)

    def get_storio_errors(self):
        return NotImplemented
