

import TeledyneLeCroyPy
import ArbRiderAWG
import matplotlib.pyplot as plt
import numpy as np

osc = TeledyneLeCroyPy.LeCroyWaveRunner('VICP::') 
awg = ArbRiderAWG.ArbRider('TCPIP::::INSTR')
TDIV=4e-3
VDIV=50e-3 

osc.set_tdiv(1,TDIV)
osc.set_tdiv(2,TDIV)
osc.set_vdiv(1,VDIV)
osc.set_vdiv(2,VDIV)

osc.set_trig_source('C1')
osc.set_trig_slope('Positive')
osc.set_trig_mode('SINGLE')
data=  osc.get_waveform(n_channel=2)

for waveform in data['waveforms']:
    time_values = waveform['Time (s)']
    amplitude_values = waveform['Amplitude (V)']

plt.plot(time_values,amplitude_values)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.title('Datos del Canal 2')
plt.grid(True)
plt.show()

