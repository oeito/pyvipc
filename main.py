import LeCroyWaveRunner
import ArbRiderAFG
import matplotlib.pyplot as plt
import numpy as np
import time



lecturas=[]

periodo= 1e-6
voltaje= 0.5
offset = 0.25
ciclos = 20

TDIV=periodo
osc.tdiv(periodo)
osc.trigMode='SINGLE'
osc.write ('CHDR OFF')
awg.ch1.output=0
awg.stop()

awg.triggerSource='MANual'
awg.ch1.output=1
awg.run()

awg.ch1.pulseConfig(1,voltaje,offset,50,periodo,0,0)

for i in range(0,ciclos,1):
    osc.trigMode='SINGLE'
    osc.opComplete()
    time.sleep(2)
    osc.waitTrigger()
    awg.trigger()
    osc.opComplete()
    lecturas.append(osc.query('C3:PAVA? WIDTH').split(',')[1])





awg.ch1.output=0
awg.stop()
awg.close()
osc.close()