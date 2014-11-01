"""Module containing classes for Storage IO-related Metrics."""

from use.base import Metrics

from linux_metrics import disk_busy

from abc import ABCMeta
from collections import namedtuple


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
        io_util_tuple = namedtuple('io_util', self._partitions)
        return io_util_tuple(disk_busy(ptn) for ptn in self._partitions)

    @property
    def saturation(self):
        """ The wait queue length of the sda is the 9th column in
            /sys/block/sda/stat."""
        wait_queue_lengths = list()
        with open("/proc/diskstats") as diskstats_file:
            line = diskstats_file.readline().split()
            if line[2] in self._partitions:
                wait_queue_lengths.append(line[11])
        return namedtuple('io_satur', self._partitions)(wait_queue_lengths)

    @property
    def get_storio_errors(self):
        raise NotImplementedError
