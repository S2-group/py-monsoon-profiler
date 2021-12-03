# py-monsoon-profiler
Python program used to get readings via the Monsoon HV Power Monitor

*Currently Work-In-Progress*

## Requirements
The only requirement for this project is a working Python 3 installation. At the moment this has been only tested on MacOS Big Sur 11.5.2 running Python version 3.9.4 .


## Installation instructions
Run the following commands in your Terminal to download the source code and to install it's dependencies:

```
$ # Clone the source code of py-monsoon-profiler
$ git clone https://github.com/S2-group/py-monsoon-profiler.git

$ # Move into the project's directory
$ cd py-monsoon-profiler

```

You can either use pip or the installer for the next steps

Using pip: `$ pip install monsoon`

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
Before being able to get readings from the device, it's serial number need to be put into the code, this can be found at the bottom of the code in the main function. On the device it can be found at the back.

From main we will call a function `testHVPM(HVPMSerialNo,pmapi.USB_protocol())` which will contain the neccesary code to get readings, it will take two parameters, the Serial Number and USB protocol.


```
def main():
    HVPMSerialNo = 12345    # Enter your device's serial number here.
    testHVPM(HVPMSerialNo,pmapi.USB_protocol()) 

```

Inside the `testHVPM()` function we will begin by defining some variables and setting up the USB.

```
    HVMON = HVPM.Monsoon()
    HVMON.setup_usb(serialno,Protocol)
    HVMON.fillStatusPacket()
```

Once this is defined we are ready to begin getting readings.

To start we will enable Vout, to send current to the main channel, this is only neccesary if you are working with the main channel and can be skipped if you are not.

`HVMON.setVout(5) # Setting Voltage to 5` 

To enable reading samples we create a variable called HVengine which will be used to enable/disable channels as well as print readings.

`HVengine = sampleEngine.SampleEngine(HVMON)`

To print readings to a csv file we can write: `HVengine.enableCSVOutput("Output.csv")`
To print readings to the Console we use: `HVengine.ConsoleOutput(True)`

In order to enable/disable channels we use the function `HVengine.enableChannel()` or `HVengine.disableChannel()`

There are 4 channels you can use(Main,USB,Aux,TimeStamp), for Main & USB, you must enable both Current & Voltage.

Enable Main:

```
    HVengine.enableChannel(sampleEngine.channels.MainCurrent)    
    HVengine.enableChannel(sampleEngine.channels.MainVoltage)
```

Enable USB:
```
    HVengine.enableChannel(sampleEngine.channels.USBCurrent)            
    HVengine.enableChannel(sampleEngine.channels.USBVoltage)
```

**Note that Main is on by default and if you must manually disable it.

In order to get the timestamps for each reading you must enable timestamps 
```
HVengine.enableChannel(sampleEngine.channels.timeStamp)
```
For USB there is one extra step which is enabling USB Passthrough, it defaults to Auto which can cause errors, so set it to On.
```
   HVMON.setUSBPassthroughMode(op.USB_Passthrough.On)
```

At this stage everything is setup for readings, you need only to begin sampling

To set the amount of samples to be taken you can use create a constant and initialize it to a value, 5000 samples is equivalent to 1 second.
To set it to an infinite amount use `numSamples=sampleEngine.triggers.SAMPLECOUNT_INFINITE`

You can set triggers for when to start/stop sampling using 
```
   HVengine.setStartTrigger(sampleEngine.triggers.GREATER_THAN,0) # Start after reading of 0
   HVengine.setStopTrigger(sampleEngine.triggers.GREATER_THAN,5) # Stop after reading of 5
```

To begin sampling you can use: `HVengine.startSampling(numSamples)`

This will run infinitly until trigger conditions have been met.

Now that triggers have been set, we can actually start sampling using:

```
    HVengine.startSampling(numSamples) 
    HVengine.disableCSVOutput()
    HVengine.startSampling(numSamples)
```
This will get the samples and automatically save them to the aforementioned CSV file.

When finished you can close the device using `HVMON.closeDevice()`


To get samples periodically we can use the built in function "periodicStartSampling"

```
HVengine.periodicStartSampling()
 for i in range(5):
        #Collect the most recent 100 samples
        samples = HVengine.periodicCollectSamples(100) 
        #samples has the same format as returned by getSamples(): [[timestamp], [mainCurrent], [usbCurrent], [auxCurrent], [mainVolts],[usbVolts]]
        print("iteration " + repr(i) + " samples collected " + repr(len(samples[0])))
        time.sleep(1) #Represents doing something else for a bit.
        
HVengine.periodicStopSampling()

```




After everything is done, the file can be run using `python3 file.py`

## Issues

When getting readings via USB power, the Hvpm delivers 4.7V instead of 5V. This causes devices such as the Raspberry Pi to give a low power warning,
however doesn't hinder the operation of the device. This issue is still awaiting a fix.
## Contributions

Any feedback, questions, and improvements about the project are very welcome, feel free to create an issue or pull request directly in this GitHub repository.



