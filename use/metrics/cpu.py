from abc import ABCMeta, abstractproperty
from os import getloadavg

from use.metrics.base import Metrics

from psutil import cpu_percent


class CpuMetrics(Metrics):

    __metaclass__ = ABCMeta

    @abstractproperty
    def utilization_per_core(self):
        pass


class LinuxCpuMetrics(CpuMetrics):
    """CPU metrics for Linux systems are obtained here."""

    @property
    def utilization(self):
        return cpu_percent()  # Not blocking but should be called every 0.1 s

    @property
    def utilization_per_core(self):
        return cpu_percent(percpu=True)

    @property
    def saturation(self):
        """Returns: (load average for 1 min, load average for 5 minutes,
           load average for 15 minutes and number of cpu cores).

           The figures  represent  the run-queue length of the CPUs.

           Note:  Linux load averages include tasks in the uninterruptable
           state (usually I/O)."""
        return getloadavg()  # TODO Support scheduler latency (perf-sched ?)

    @property
    def errors(self):
        raise NotImplementedError
