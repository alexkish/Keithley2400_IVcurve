#################
import serial
import time
import sys
import os
import array as arr
import matplotlib.pyplot as plt
import numpy as np
import h5py


#################
# Keithley 2400 #
#################
# USING PYMEASURE LIBRARY ONLY
from pymeasure.instruments.keithley import Keithley2400
# LIST ALL RESOURCES
from pymeasure.instruments import list_resources
#list_resources()

#print('Instruments connected.')

# CREATE OUT DIR AND FILE OUTPUT
#outputdir = './plots/'
outputdir = '/Users/alexkish/Documents/Fermilab/PAB/Monochromator/controls/plots'
print('Output directory:', outputdir)
isExist1 = os.path.exists(outputdir)
if isExist1=='False':
    os.mkdir(outputdir)
    
# CONNECT TO KEITHLEY
keithley = Keithley2400("ASRL1::INSTR", timeout=2000, baud_rate=57600)

keithley.read_termination = "\n"
keithley.write_termination = "\n"

# IDENTIFY KEITHLEY INSTRUMENT
keithley.write("*IDN?")
keithley.read()

# SWITCH ON KEITHLEY AND SET IT UP
keithley.compliance_current = 100e-6        # Sets the compliance current
keithley.source_voltage = -15.0           # Volt
keithley.enable_source()
keithley.source_current_range = 100e-6    # Ampere
keithley.current_range = 100e-6    # Ampere
#keithley.auto_range_source()
keithley.auto_zero = False
keithley.check_get_errors=False
keithley.check_set_errors=False
#keithley.display_enabled=False

#keithley.source_current = 0             # Sets the source current to 0 mA
#keithley.enable_source() 

keithley.wait_for(query_delay=4.0)
#keithley.wait_for_buffer(should_stop=False, timeout=60, interval=0.1)

keithley.timeout = None
keithley.write_timeout = None
del keithley.timeout

##########################
keithley.measure_current(nplc=1.0, current=100e-6, auto_range=False)

print('PD current = ', keithley.current, 'A')

V_start = 0
V_end = 55
V_delta = 1
N_points = (V_end-V_start)/V_delta
scan_delay = 0.1

voltage = arr.array('d')
current = arr.array('d')

print('V    I')
#START SCAN IN POSITIVE DIRECTION
for step in range(int(N_points)):
    setV = -(V_start + step*V_delta)
    keithley.source_voltage = setV
    
    keithley.enable_source()
	keithley.measure_current(nplc=1.0, current=100e-6, auto_range=False)
    print('V=', setV, 'I=', keithley.current)
    
    time.sleep(scan_delay)
    SiPMvoltage = setV*(-1)
    SiPMcurrent = keithley.current*(-1)
    voltage.append(SiPMvoltage)
    current.append(SiPMcurrent)

# CLOSE THE SESSION
print('Finished run.')
keithley.shutdown()
