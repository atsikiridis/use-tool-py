use-tool-py
===========

An implementation of a suite of system metrics in Python as defined by the USE (Utilisation, Saturation, Errors) method. You can find more information about the USE method on Brendan Gregg's [blog-post](http://dtrace.org/blogs/brendan/2012/02/29/the-use-method/). 

About use-tool-py
=================

This suite of metrics aspires to become: 

1) accurate and efficient (most directed sources of metrics are used, when possible)
2) extendable for many systems (an Object Oriented Approach is  being followed to achieve this) 
3) easy to use ( robust shell client, informative web interface).

Currently, there are 11 USE Metrics available for a Linux system in the code. The source of the already imlemented metrics is the  *proc* filesystem  and data from *dmesg*. However, other sysadmin tools and system interfaces are being closely examined (strace, systemTap, smartctl, perf) and potentially useful data will be integrated to use-tool-py soon. For more data sources, check [this](http://dtrace.org/blogs/brendan/2012/03/07/the-use-method-linux-performance-checklist/) checklist for Linux (you can find checklists for other systems, too) by Brendan Greeg again.


Installing
==========

Note: There is not yet a "production" client to access all data. A web interface is in the short-term plans.

The project can be installed by :

```
$ git clone https://github.com/atsikiridis/use-tool-py
$ cd use-tool-py
$ sudo python setup.py install
```

For, now you can run:

```
$ usepy_example
```

To check that it works. And of course run the unit tests. More to come!


License
=======

The project is available under the GNU V 2.0 License.
