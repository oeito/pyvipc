import LeCroyWaveRunner
import ArbRiderAFG
import matplotlib.pyplot as plt
import numpy as np
import time




lecturas1=[]
lecturas2=[]

periodo= 1000e-9
voltaje= 0.5
offset = 0
ciclos = 1000
duty= 50


TDIV=periodo
osc.tdiv(TDIV)
osc.trigMode='AUTO'
osc.write('CLEAR_SWEEPS')

osc.ch3.vdiv=0.5
osc.ch4.vdiv=0.5
osc.ch3.trigLevel=0.5
osc.ch4.trigLevel=0.5
osc.parameterSetup('WID',1,3)
osc.parameterSetup('WID',2,4)

awg.ch1.shape='PULSe'
awg.ch1.burstState=1
awg.ch1.burstMode='TRIGgered'
awg.ch1.burstNcycles=1

awg.ch2.shape='PULSe'
awg.ch2.burstState=1
awg.ch2.burstMode='TRIGgered'
awg.ch2.burstNcycles=1

awg.triggerSource='MANual'
awg.ch1.output=1
awg.ch2.output=1
awg.run()
time.sleep(1)
awg.ch1.pulseConfig(1,voltaje,offset,50,periodo,0.8e-9,0.8e-9)
awg.ch2.pulseConfig(1,voltaje,offset,50,periodo,0.8e-9,0.8e-9)

for i in range(0,ciclos):
    osc.trigMode='SINGLE'
    osc.opComplete()
    osc.waitTrigger()
    time.sleep(0.5)
    awg.trigger()
    osc.opComplete()
    valor1=osc.query('C3:PAVA? WIDTH ').split(',')[1]
    valor2=osc.query('C4:PAVA? WIDTH ').split(',')[1]

    lecturas1.append(float(valor1))
    lecturas2.append(float(valor2))

plt.hist(lecturas1, bins=10, density=True, color='skyblue', edgecolor='black')

plt.show()
# Añadir etiquetas y título
plt.xlabel('Valores')
plt.ylabel('Densidad de probabilidad')
plt.title('Histograma de valores normalizado')

# Mostrar el histograma
plt.show()

awg.ch1.burstState=0
awg.ch1.output=0
awg.stop()
awg.close()
osc.close()