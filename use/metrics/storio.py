"""Module containing classes for Storage IO-related Metrics."""
from abc import ABCMeta

from linux_metrics import disk_busy

from use.metrics.base import Metrics


class StorageIOMetrics(Metrics):
    """Abstract base class for Storage IO  metrics. All implementations
        (depending on OS) should implement the abstract methods defined here."""

    __metaclass__ = ABCMeta


class LinuxStorageMetrics(StorageIOMetrics):
    """Network metrics for Linux Systems are obtained here."""

    def __init__(self):
        with open("/proc/partitions") as partitions_file:
            lines = partitions_file.readlines()[2:]
            self._partitions = (line.split()[2] for line in lines)

    @property
    def utilization(self):  # per device
        return (disk_busy(ptn) for ptn in self._partitions)

    @property
    def saturation(self):
        """ The wait queue length of the sda is the 9th column in
            /sys/block/sda/stat."""
        wait_queue_lengths = list()
        with open("/proc/diskstats") as diskstats_file:
            for line in diskstats_file:
                tokens = line.split()
                if tokens[2] in self._partitions:
                    wait_queue_lengths.append((tokens[2], tokens[11]))
        return tuple(wait_queue_lengths)

    @property
    def errors(self):
        raise NotImplementedError
