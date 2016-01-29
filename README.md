UShareSoft UForge AppCenter CLI
=====

A command-line tool to interact with the UForge AppCenter webservice. 

Installation
============
uforgecli is based on python, consequently it supports all major operating systems.  The easiest way to install uforgecli is using `pip`.

```
$ pip install uforgecli 
```

Installing From Source
======================
Clone the uforge-cli git repository to get all the source files.
Next go to the source directory where the `setup.py` file is located.
To compile and install, run (as sudo):

```
$ sudo python setup.py build install
```

This will automatically create the uforgecli executable and install it properly on your system.

To check that this was successful, run:

```
$ uforge —v 
```

Upgrading
=========
If you have already installed uforgecli, and you wish to upgrade to the latest version, use:
```
$ pip install —upgrade uforgecli
```

License
=======
uforgecli is licensed under the Apache 2.0 license. For more information, please refer to LICENSE file.
