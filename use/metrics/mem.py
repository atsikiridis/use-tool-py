""" Module containing classes for Memory Capacity MEtrics."""
from __future__ import division

from psutil import virtual_memory
from psutil import swap_memory

from use.metrics import MemoryMetrics, metric

@metric('Linux')
class LinuxMemoryMetrics(MemoryMetrics):
    """Memory metrics for Linux Systems are obtained here."""

    @property
    def utilization(self):
        memory = virtual_memory()
        return memory.available / memory.total

    @property
    def saturation(self):
        return swap_memory().percent  # TODO Thread swapping

    @property
    def errors(self):
        """Memory Errors, as output of dmesg err.
           TODO systemtap malloc probes."""
        raise NotImplementedError
