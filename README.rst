Angus.ai on JumpingSumo robot
=============================

This is a sample code just for fun: enjoy !

Big picture
-----------

Network configuration
+++++++++++++++++++++

You need a computer with two interfaces with one wifi (at least).

.. parsed-literal::
  JumpingSumo <===Wifi(LAN)===> Computer (wrapper.py) <===Ethernet(WAN)===> Angus.ai

Quick & dirty
+++++++++++++

After trying to bind ARDroneSDK3 in python (epic fail), I just "wrap" the executable with python ``subprocess.Popen`` and I simulate keystrokes by communicating to the process through ``stdin`` pipe for commands and use the fifo for video streaming.

Installation
------------

**Download and install ARDoneSDK3**:

1. Go to https://github.com/ARDroneSDK3/ARSDKBuildUtils

2. Follow the instructions

**Compile the driver**::

  $ git clone https://github.com/angus-ai/angus-jumpingsumo.git
  $ cd angus-jumpingsumo
  $ make

**Prepare the environment**::

  $ cd angus-jumpingsumo
  $ virtualenv env
  $ source env/bin/activate
  $ pip install angus-sdk-python

**Run**:

1. Connect your jumping sumo to your computer
2. execute ``./wrapper.py``

Discussion and support
----------------------

You can discuss Angus SDK on `the Angus SDK developer mailing list <https://groups.google.com/d/forum/angus-sdk-python-dev>`_, and report bugs on the `GitHub issue tracker <https://github.com/angus-ai/angus-sdk-python/issues>`_.

This web site and all documentation is licensed under `Creative
Commons 3.0 <http://creativecommons.org/licenses/by/3.0/>`_.

Angus Python SDK is Angus.ai open source technologies It is available under the `Apache License, Version 2.0. <https://www.apache.org/licenses/LICENSE-2.0.html>`_. Please read LICENSE and NOTICE files for more information.

Copyright 2015, Angus.ai
