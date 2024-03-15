import pyvisa
import numpy as np
import time


LIMITS = {
	'freqLim': 1,
	'volLim': 2,
	'wavelengthLim': 4, 
	'resolutionLim': 4,
	'memLocLim': 2,
}


class ArbRider:
        def __init__(self,resource_name:str):
                try:
                        rm=pyvisa.ResourceManager('@py')
                        self.rm=rm.open_resource(resource_name)
                except:
                        print('Pyvisa not installed')
                        raise
                self.ch1= self.Channel(self.rm,1)
                self.ch2= self.Channel(self.rm,2)
     
        def __del__(self):
                self.rm.close()    
                 
        def write(self, msg):
                self.rm.write(msg)
                time.sleep(0.1)

        def writeBinary(self,command:str,values:str):
                self.rm.write_binary_values(command, values, datatype='d', is_big_endian=False)

        def close(self):
                self.rm.close()

        def query(self, msg):
                return self.rm.query(msg)
                time.sleep(0.1)
        
        def idn(self):
                return self.query('*IDN?')
        
        def syncroniseChannels(self):
                self.write('PHAS:INIT')

        def setCustomWaveform(self, waveform:np.array,name:str):
                self.write(f'WLISt:WAVeform:NEW "{name}",{waveform.length},REAL')
                self.writeBinary(f'WLISt:WAVeform:DATA "{name}",0,{waveform.length}', waveform )
        


        @property
        def runState(self):
                """Query run status      
                Returns
                ------------
                int
                        0 indicates that the instrument has stopped.
                        1 indicates that the instrument is waiting for trigger.
                        2 indicates that the instrument is running.
                """
                return self.query(f'RSTate?')    

        def run(self):
                self.write(f'AFGControl:START')    
  
        def stop(self):
                self.write(f'AFGControl:STOP')    

        def trigger(self):
                self.write(f'TRIGger:SEQuence:IMMediate ')    

        ## Setters ################################################
 

        class Channel:
                def __init__(self,awg,channel:int):
                        self._awg=awg
                        self._channel=channel
                        self._output=0
                        self._amplitude=0
                        self._pulseWidth=0
                        self._pulseDutyCycle=0
                        self._runMode=0
                        self._trigger=0
                        self._burst=0
                ## Properties #############################################
                        


                ## Setters ################################################


                def amplitude(self,value:float):
                        if value != self._amplitude:
                                self._amplitude=value
                                self._awg.write(f'SOURce{self._channel}:VOLTage:LEVel {value}')

                def shape(self,value:str):
                        if value != self._shape:
                                self._shape=value
                                self._awg.write(f'SOURce{self._channel}:WAVeform {value}')
   
                def frequency(self,value:int):
                        if value != self._frequency:
                                self._frequency=value
                                self._awg.write(f'SOURce{self._channel}:FREQuency:FIXed {value}')
 
                def offset(self,value:float):
                        if value != self._offset:
                                self._offset=value
                                self._awg.write(f'SOURce{self._channel}:VOLTage:LEVel:OFFSet {value}')

                def phase(self,value:int):
                        if value!=self._phase:
                                self._phase=value
                                self._awg.write(f'OUTPut{self._channel}:PHASe:ADJust {value}')         
         
                def output(self,value:int):
                        if value!=self._output:
                                self._output=value
                                self._awg.write(f'OUTPut{self._channel}:STATe {value}')         
          
                def sync(self,value:int):
                        if value!=self._sync:
                                self._sync=value
                                self._awg.write(f'SOURCE{self._channel}:FREQuency:CONCurrent {value}')   

                def burst(self,value:int):
                        if value!=self._burst:
                                self._burst=value
                                self._awg.write(f'SOURCE{self._channel}:BURSt:STATe {value}')   



               
                def pulseDutyCycle(self,value:int):
                        if value!=self._pulseDutyCycle:
                                self._pulseDutyCycle=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:DCYCle {value}')      

        
                def pulsePeriod(self,value:int):
                        if value!=self._pulsePeriod:
                                self._pulsePeriod=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:PERiod {value}')      

       
                def pulseTransition(self,value:int):
                        if value!=self._pulseTransition:
                                self._pulseTransition=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:TRANsition {value}')      

          
                def pulseWidth(self,value:int):
                        if value!=self._pulseWidth:
                                self._pulseWidth=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:WIDTh {value}')      
                def runMode(self,mode:str):
                        """Set run mode       
                        Parameterers
                        ------------
                        mode : str
                                CONTinuous sets Run Mode to Continuous.
                                TRIGgered sets Run Mode to Triggered.
                                GATed sets Run Mode to Gated.
                                SEQuence sets Run Mode to Sequence
                        """
                        if mode!=self._runMode:
                                self._runMode=mode
                                self._awg.write(f'SOURCE{self._channel}:RMODE {mode}')        
                ## Functions #############################################