import Monsoon.HVPM as HVPM
import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine
import Monsoon.Operations as op
import Monsoon.pmapi as pmapi
import numpy as np

def testHVPM(serialno=None,Protocol=pmapi.USB_protocol()):
    HVMON = HVPM.Monsoon()
    HVMON.setup_usb(serialno,Protocol)
    print("HVPM Serial Number: " + repr(HVMON.getSerialNumber()))
    HVMON.fillStatusPacket()
    HVMON.setVout(5)
    HVengine = sampleEngine.SampleEngine(HVMON)
    #Output to CSV
    HVengine.enableCSVOutput("HV Output.csv") 
    #Turning off periodic console outputs.
    HVengine.ConsoleOutput(True)


    #Setting all channels enabled
    HVengine.enableChannel(sampleEngine.channels.MainCurrent)         # Main Channel
    HVengine.enableChannel(sampleEngine.channels.MainVoltage)

    # HVengine.disableChannel(sampleEngine.channels.MainCurrent)          # Uncomment to disable Main Current
    # HVengine.disableChannel(sampleEngine.channels.MainVoltage)    

    # USB Channel
    HVengine.enableChannel(sampleEngine.channels.USBCurrent)            
    HVengine.enableChannel(sampleEngine.channels.USBVoltage)

    # Aux Channel
    HVengine.enableChannel(sampleEngine.channels.AuxCurrent)     
     
    HVengine.enableChannel(sampleEngine.channels.timeStamp)


    HVMON.setUSBPassthroughMode(op.USB_Passthrough.On)  # Allows power to the HVPM USB ports

    #Setting trigger conditions
    numSamples=sampleEngine.triggers.SAMPLECOUNT_INFINITE      # numSamples = 5000 is one second of sampling 

    HVengine.setStartTrigger(sampleEngine.triggers.GREATER_THAN,0) # Determine when to begin readings
    # HVengine.setStopTrigger(sampleEngine.triggers.GREATER_THAN,5) # Determine when to stop readings

    HVengine.setTriggerChannel(sampleEngine.channels.timeStamp) 

    #Actually start collecting samples
    HVengine.startSampling(numSamples)
    #startSampling() continues until the trigger conditions have been met, and then ends automatically.
    #Measurements are automatically saved to the filename passed in enableCSVOutput()

    #Disable CSV Output
    HVengine.disableCSVOutput()
    #Collect another 5 seconds worth of samples
    HVengine.startSampling(numSamples)
    #Get those samples as a Python list
    samples = HVengine.getSamples()
    #Samples has the format  [[timestamp], [mainCurrent], [usbCurrent], [auxCurrent], [mainVolts],[usbVolts]]
    #Use sampleEngine.channel to select the appropriate list index.
    timestamp = samples[sampleEngine.channels.timeStamp]
    mainCurrent = samples[sampleEngine.channels.MainCurrent]
    auxCurrent = samples[sampleEngine.channels.AuxCurrent]
    usbCurrent = samples[sampleEngine.channels.USBCurrent]
    mainVoltage = samples[sampleEngine.channels.MainVoltage]
    usbVoltage = samples[sampleEngine.channels.USBVoltage]

    #Perform analysis on the resulting data.  For example, in order to calculate, perform the following:
    #mainCurrent is given in mA.  Divide by 1000 to convert to Amps
    scaledMainCurrent = [x / 1000 for x in mainCurrent]
    #Element-wise multiply to produce Watts. Power = Current * Voltage.  
    mainPower = np.multiply(scaledMainCurrent, mainVoltage) 

    #When finished, close the device.
    HVMON.closeDevice();

def main():
    HVPMSerialNo = 23171    # Enter your device's serial number here (Sticker on the back of the device)
    testHVPM(HVPMSerialNo,pmapi.USB_protocol())

if __name__ == "__main__":
    main()