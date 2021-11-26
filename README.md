# py-monsoon-profiler
Python program used to get readings via the Monsoon HV Power Monitor

*Currently Work-In-Progress*

## Requirements
The only requirement for this project is a working Python 3 installation. At the momemnt this has been only tested on MacOS Big Sur 11.5.2 running Python version 3.9.4 .


## Installation instructions
Run the following commands in your Terminal to download the source code and to install it's dependencies:

```
$ # Clone the source code of py-monsoon-profiler
$ git clone https://github.com/S2-group/py-monsoon-profiler.git

$ # Move into the project's directory
$ cd py-monsoon-profiler

```

You can either use pip or the installer for the next steps

Using pip: `$ Pip install monsoon`

Using the installer: Download the Python installer from http://msoon.github.io/powermonitor/ - unzip the contents and find setup.py.  From there, use the command:
‘Python setup.py install’

## Dependencies
The following libraries are used with this library and will need to be installed before use.

Numpy:  http://www.numpy.org/
or install using `pip install numpy`

pyUSB:  https://github.com/walac/pyusb
or install using `pip install pyusb`

libusb 1.0: http://www.libusb.org/wiki/libusb-1.0
or install using `pip install libusb1`

Note: pyUSB also supports libusb 0.1 and OpenUSB as backends, but those haven't been tested with this script and are not officially supported by Monsoon

## Preparing your environment (Windows)

On windows, for any device to be detected by libusb, you will need to install a libusb filter.  This can be downloaded from https://sourceforge.net/projects/libusb-win32/.  This step can be skipped for Linux and MacOS users. 


## Usage
Before being able to get readings from the device you need to put it's serial number into the code, this can be found at the bottom of the code in the main function. On the device it can be found at the back.

```
def main():
    HVPMSerialNo = 12345    # Enter your device's serial number here.

```

After everything is done, the file can be run using `python3 SimpleSamplingExample.py`

## Issues

When getting readings via USB power, the Hvpm delivers 4.7V instead of 5V. This causes devices such as the Raspberry Pi to give a low power warning,
however doesn't hinder the operation of the device. This issue is still awaiting a fix.
## Contributions

Any feedback, questions, and improvements about the project are very welcome, feel free to create an issue or pull request directly in this GitHub repository.



