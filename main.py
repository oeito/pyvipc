import TeledyneLeCroyPy
import ArbRiderAWG
import matplotlib.pyplot as plt
import numpy as np
import time
osc = TeledyneLeCroyPy.LeCroyWaveRunner('VICP::') 
awg = ArbRiderAWG.ArbRider('TCPIP:: ::INSTR')
TDIV=4e-3
VDIV=50e-3 

osc.set_tdiv('10us')
osc.set_vdiv(3, 50e-3)

osc.set_trig_mode('SINGLE')
osc.set_trig_source('C3')
osc.set_trig_slope('C3','Positive')

awg.ch1.burst('ON')
awg.ch1.output(1)
awg.ch1.pulseWidth('5us')
awg.ch1.amplitude(200e-3)
awg.ch1.pulseDutyCycle(20)
awg.run()
awg.trigger()
data=  osc.get_waveform(n_channel=3)
for waveform in data['waveforms']:
    time_values = waveform['Time (s)']
    amplitude_values = waveform['Amplitude (V)']
time.sleep(2)
   
awg.ch1.output(0)

awg.stop()
plt.plot(time_values,amplitude_values)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')
plt.title('Datos del Canal 2')
plt.grid(True)
plt.show()
awg.close()