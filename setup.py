"""The setup.py module of use-tool-py."""

from setuptools import setup, find_packages

setup(name="use",
      version="0.1",
      description=""" A python-based open-source implementation of a system
                        metrics tool. Based on the USE Method
                        (Utilization, Saturation, Errors).""",
      long_description=__doc__,
      author="Artem Tsikiridis",
      author_email="atsik@dmst.aueb.gr",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=["psutil", "linux-metrics", "flask"]
      )
