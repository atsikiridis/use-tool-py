from os import getloadavg
from abc import abstractproperty

from base import Metrics, metric

from psutil import cpu_percent


class CpuMetrics(Metrics):

    @abstractproperty
    def utilization_per_core(self):
        pass


@metric('Linux')
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


#@metric('FreeBSD')
#class FreeBSDCpuMetrics(LinuxCpuMetrics):
#    pass
