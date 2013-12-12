""" Module containing classes for Memory Capacity MEtrics."""

from abc import ABCMeta, abstractmethod
from usetool.sys_util import Metric, SystemUtilities
import subprocess

class MemoryMetrics(object):
    """Abstract base class for Memory metrics. All implementations
        (depending on OS) should implement the abstract methods defined here."""

    __metaclass__ = ABCMeta


    def __new__(cls):
        return SystemUtilities.get_metric_obj(cls)

    @abstractmethod
    def get_mem_util(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Memory Utilisation metrics. """
        return NotImplemented

    @abstractmethod
    def get_mem_satur(self):
        """Abstract method. Should be implemented by subclasses
            to obtain Memory Saturation metrics. """
        return NotImplemented

    @abstractmethod
    def get_mem_errors(self):
        """Abstract methos. Should be implemented by subclasses
            to obtain Memory Errors metrics."""
        return NotImplemented

@Metric('Linux')
class LinuxMemoryMetrics(MemoryMetrics):
    """Memory metrics for Linux Systems are obtained here."""

    def get_mem_util(self):
        """ Memory utilization in Linux is based on /proc/meminfo.
            Total Memory and Free Memory are used."""
        with open("/proc/meminfo") as meminfo_file:
            total_mem  = meminfo_file.next().split(":")[1] #Not numeric.
            total_mem =  SystemUtilities.get_numeric_value(total_mem) #Numeric.
            free_mem = meminfo_file.next().split(":")[1]
            free_mem = SystemUtilities.get_numeric_value(free_mem)
        return str((1 - free_mem / total_mem) * 100)

    def get_mem_satur(self):
        """Memory saturation in Linux is based on dmesg.
           We are interested in 'killed' processes
           or the invocations of the OOM killer."""
        shell1 = subprocess.Popen(['dmesg'], stdout = subprocess.PIPE)
        shell2 = subprocess.Popen(['egrep', '-i', 'killed'],
                 stdin = shell1.stdout)
        killedprocs  = shell2.communicate()[0]
        if not killedprocs:
            return "OOM Killer has not been invoked."
        else:
            proc_ids = []
            for line in killedprocs:
                tokens =  line.split(" ")
                proc_ids.append(tokens[tokens.index("process") + 1])
            return proc_ids

    def get_mem_errors(self):
        """Memory Errors, as output of dmesg err.
           TODO systemtap malloc probes."""
        return subprocess.Popen(['dmesg', '-H', '-l', 'err'])
