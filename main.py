
import TeledyneLeCroyPy
import ArbRiderAWG
import matplotlib.pyplot as plt
import numpy as np

o = TeledyneLeCroyPy.LeCroyWaveRunner('VICP::') 
awg = ArbRiderAWG.ArbRider('VICP::')
TDIV=4e-3
VDIV=50e-3 

o.set_tdiv(1,TDIV)
o.set_tdiv(2,TDIV)
o.set_vdiv(1,VDIV)
o.set_vdiv(2,VDIV)

o.set_trig_source('C1')
o.set_trig_slope('Positive')
o.set_trig_mode('SINGLE')
data=  o.get_waveform(n_channel=2)
for waveform in data['waveforms']:
    time_values = waveform['Time (s)']
    amplitude_values = waveform['Amplitude (V)']


plt.plot(time_values,amplitude_values)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.title('Datos del Canal 2')
plt.grid(True)
plt.show()


