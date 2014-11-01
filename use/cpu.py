"""Module providing classes for CPU metrics
    (Utilisation, Saturation, Errors)."""

from abc import ABCMeta, abstractproperty
import time
from use.sys_util import Metric, SystemUtilities


class CpuMetrics(object):
    """Abstract base class for CPU metrics. All implementations
        (depending on OS) should implement the abstract methods defined here."""

    __metaclass__ = ABCMeta

    def __new__(cls):
        """Returns appropriate implementation of Metric"""
        return SystemUtilities.get_metric_obj(cls)

    @abstractproperty
    def utilization(self):
        """Abstract method. Should be implemented by subclasses
            to obtain CPU Utilisation metrics. """
        return NotImplemented

    @abstractproperty
    def saturation(self):
        """Abstract method. Should be implemented by subclasses
            to obtain CPU Saturation metrics. """
        return NotImplemented

    @abstractproperty
    def errors(self):
        """Abstract method. Should be implemented by subclasses
            to obtain CPU Errors metrics. """
        return NotImplemented

@Metric('Linux')
class LinuxCpuMetrics(CpuMetrics):
    """CPU metrics for Linux systems are obtained here."""

    INTERVAL = 2 # Arbitrary value of seconds (delta). Subject to change.

    def get_cpu_util(self):
        """Get Linux CPU Utilisation based on /proc/stat.
           cpu_usage(t) = 100% * ( total(t) - total(t - dt) +
           idle(t) - idle(t-dt) ) / total(t) - total(t -dt

           where:
           total(t) = user(t) + nice(t) + system(t) + idle(t)
           (From left to right the columns of  $(cat /proc/stat | head -n 1)
           and
           dt an arbitrary seconds interval ( currently 2  seconds)"""

        delta_time = LinuxCpuMetrics._delta_time(self.INTERVAL)
        return 100 - (delta_time[len(delta_time) - 1] * 100.00 /
        sum(delta_time))

    @classmethod
    def _delta_time(cls, interval):
        """dt is calculated for every column according to the specified seconds
            interval."""
        first_event = LinuxCpuMetrics._get_time_list()
        try:
            time.sleep(interval)
        except IOError:
            raise ValueError("Invalid value for INTERVAL (must be positive)")
        second_event = LinuxCpuMetrics._get_time_list()
        for i in range(len(first_event)):
            second_event[i] -= first_event[i]
        return second_event

    @classmethod
    def _get_time_list(cls):
        """The time_list is being produced. """
        stat_file = file("/proc/stat", "r")

        #The first name column (cpu) and the other extra columns
        #(after idle) are omitted.

        time_list = stat_file.readline().split(" ")[2:6]
        stat_file.close()

        for i in range(len(time_list)):
            time_list[i] = int(time_list[i])
        return time_list

    def get_cpu_satur(self):
        """Returns: (load average for 1 min, load average for 5 minutes,
           load average for 15 minutes and number of cpu cores).

           The figures  represent  the run-queue length of the CPUs.

           Note:  Linux load averages include tasks in the uninterruptable
           state (usually I/O)."""
        loadavg_file = file("/proc/loadavg", "r")

        #load average three values
        loadavg_val = loadavg_file.readline().split(" ")[0:3]
        loadavg_file.close()
        saturdict = {}
        saturdict["loadavg1min"] = float(loadavg_val[0])
        saturdict["loadavg5min"] = float(loadavg_val[1])
        saturdict["loadavg15min"] = float(loadavg_val[2])
        cpuinfo_file = file("/proc/cpuinfo", "r")
        no_cores = 12 #The metric we need is on the 12th line of the file
        for index, current in enumerate(cpuinfo_file):
            if index == no_cores:
                no_cores = int(current.split(": ")[1])
                break
        cpuinfo_file.close()
        saturdict["no_cores"] = no_cores
        return saturdict

    def get_cpu_errors(self):
        return NotImplemented

