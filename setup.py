"""The setup.py module of use-tool-py."""

from distutils.core import setup
import glob

setup(name = "use-tool-py",
      version = "0.1",
      description = """ A python-based open-source implementation of a system
                        metrics tool. Based on the USE Method
                        (Utilisation, Saturation, Errors).""",
      author = "Artem Tsikiridis",
      author_email = "atsik@dmst.aueb.gr",
      packages = ["usetool"],
      scripts = glob.glob('bin/usepy_example')
      )