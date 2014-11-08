"""Module with utilities for system_awareness and reusable code."""



class SystemUtilities(object):
    """Reusable functionality for the USE tool."""

    @staticmethod
    def get_metric_obj(baseclass):
        """Returns the appropriate implementation of a metric.
           Abstract Base classes should call this in __new__."""
        cls = SYSMAP.get(platform.system())
        if not cls:
            raise RuntimeError("No metric class found!")
        elif cls is baseclass:
            return object.__new__(baseclass)
        elif issubclass(cls, baseclass) :
            return cls()
        else:
            raise RuntimeError(str(baseclass) +
                  "is not a base class for a metric.")

    @staticmethod
    def get_numeric_value(inputstr):
        """This private method gets a non numeric String
           and returns the numbers only. For example:
           if input is '       52   kb \n ' this method returns 52.0
           as a float."""
        try:
            return float([float(s) for s in inputstr.split() if s.isdigit()][0])
        except IndexError:
            raise ValueError(inputstr + " has no digits.")
