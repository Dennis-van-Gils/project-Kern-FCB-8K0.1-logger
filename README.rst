.. image:: https://img.shields.io/github/v/release/Dennis-van-Gils/project-Kern-FCB-8K0.1-logger
    :target: https://github.com/Dennis-van-Gils/project-Kern-FCB-8K0.1-logger
    :alt: Latest release

Kern FCB 8K0.1 balance logger
=============================

Logs the weight readings from a Kern FCB 8K0.1 balance via the RS232 port to a
file on disk. Features a minimalistic interface running inside the terminal.

The acquisition rate is as fast as the balance allows, approximately at 4
readings per second. The log file contains three columns as follows:

    * Column 1: Time stamp in seconds
    * Column 2: Weight reading
    * Column 3: Weight unit

Note that the weight unit gets omitted by the Kern balance whenever it deems the
weight readout to be unstable. This happens at fluctuating loads.

Instructions
============
Download the `zip file <https://github.com/Dennis-van-Gils/project-Kern-FCB-8K0.1-logger/releases/latest>`_
containing the Python scripts and unpack to a folder onto your drive.

Open a Python terminal (i.e. `Anaconda prompt` when you are using the Anaconda
Python distribution) and navigate to the folder you just unpacked.

Run the following inside your Python terminal to install the necessary
packages. *This is only needed once*:

    ::

        pip install -r requirements.txt

Now you're ready to start the program by running:

    ::

        python main.py