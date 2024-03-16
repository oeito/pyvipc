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
        
        def idn(self):
                return self.query('*IDN?')
        
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
                self.write(f'TRIGger:IMMediate')    

        @property
        def triggerTimer(self):
                self.write(f'TRIGger:TIMer?')    
        @triggerTimer.setter
        def triggerTimer(self, value:float):
                if value!=self._triggerTimer:
                        self._triggerTimer=value
                self.write(f'TRIGger:TIMer {value}')      
        @property
        def triggerSource(self):
                return self.query(f'TRIGger:SOURce?')    
        @triggerSource.setter
        def triggerSource(self, mode:str):
                if mode!=self._triggerSource:
                        self._triggerSource=mode
                return self.write(f'TRIGger:SOURce {mode}')      
             
        ## Setters ################################################
 

        class Channel:
                def __init__(self,awg,channel:int):
                        self._awg=awg

                @property
                def output(self):
                        return self._awg.query(f'OUTPut{self._channel}:STATe?')

                @output.setter       
                def output(self,value:int):
                        if value!=self._output:
                                self._output=value
                                self._awg.write(f'OUTPut{self._channel}:STATe {value}')           
                @property
                def outputDelay(self):
                        return self._awg.query(f'OUTPut{self._channel}:DELay?')
                @outputDelay.setter       
                def outputDelay(self,value:int):
                        if value!=self._outputDelay:
                                self._outputDelay=value
                                self._awg.write(f'OUTPut{self._channel}:DELay {value}')           
                @property
                def outputImpedance(self):
                        return self._awg.query(f'OUTPut{self._channel}:IMPedance?')
                @outputImpedance.setter       
                def outputImpedance(self,value:int):
                        if value!=self._outputImpedance:
                                self._outputImpedance=value
                                self._awg.write(f'OUTPut{self._channel}:IMPedance {value}')       
                @property
                def outputLoad(self):
                        return self._awg.query(f'OUTPut{self._channel}:LOAd?')
                @outputLoad.setter       
                def outputLoad(self,value:int):
                        if value!=self._outputLoad:
                                self._outputLoad=value
                                self._awg.write(f'OUTPut{self._channel}:LOAd {value}')       
                @property
                def outputLowImpedance(self):
                        return self._awg.query(f'OUTPut{self._channel}:LOW:IMPedance?')
                @outputLowImpedance.setter       
                def outputLowImpedance(self,value:int):
                        if value!=self._LowImpedance:
                                self._LowImpedance=value
                                self._awg.write(f'OUTPut{self._channel}:LOW:IMPedance {value}')   
                @property
                def frequency(self):
                        return self._awg.query(f'SOURce{self._channel}:FREQuency?')
                @frequency.setter  
                def frequency(self,value:int):
                        if value != self._frequency:
                                self._frequency=value
                                self._awg.write(f'SOURce{self._channel}:FREQuency {value}')
                @property
                def shape(self):
                        return self._awg.query(f'SOURce{self._channel}:FUNCtion:SHAPe?')
                @shape.setter
                def shape(self,value:str):
                        if value != self._shape:
                                self._shape=value
                                self._awg.write(f'SOURce{self._channel}::FUNCtion:SHAPe {value}')
                @property
                def phase(self):
                        return self._awg.query(f'SOURce{self._channel}:PHASe?') 
                @phase.setter
                def phase(self,value:int):
                        if value!=self._phase:
                                self._phase=value
                                self._awg.write(f'OUTPut{self._channel}:PHASe {value}')        
                @property
                def runMode(self):
                        return self._awg.query(f'SOURce{self._channel}:RUNMode?') 
                @runMode.setter
                def runMode(self,mode:str):
                        if mode!=self._runMode:
                                self._runMode=mode
                                self._awg.write(f'SOURCE{self._channel}:RUNMode {mode}')            
                @property
                def amplitude(self):
                        return self._awg.query(f'SOURce{self._channel}:VOLTage:AMPLitude?')
                @amplitude.setter
                def amplitude(self,value:float):
                        if value != self._amplitude:
                                self._amplitude=value
                                self._awg.write(f'SOURce{self._channel}:VOLTage:LEVel {value}')
                @property
                def offset(self):
                        return self._awg.query(f'SOURce{self._channel}:VOLTage:OFFSet?')
                @offset.setter
                def offset(self,value:float):
                        if value != self._offset:
                                self._offset=value
                                self._awg.write(f'SOURce{self._channel}:VOLTage:LEVel:OFFSet {value}')
                @property
                def pulseDutyCycle(self):
                        return self._awg.query(f'SOURce{self._channel}:PULSe:DCYCle?')      

                @pulseDutyCycle.setter
                def pulseDutyCycle(self,value:int):
                        if value!=self._pulseDutyCycle:
                                self._pulseDutyCycle=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:DCYCle {value}')   
                @property
                def pulsePeriod(self):
                        return self._awg.query(f'SOURce{self._channel}:PULSe:PERiod?')      

                @pulsePeriod.setter
                def pulsePeriod(self,value:int):
                        if value!=self._pulsePeriod:
                                self._pulsePeriod=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:PERiod {value}')     
                @property
                def pulseTransitionLead(self):
                        return self._awg.query(f'SOURce{self._channel}:PULSe:TRANsition:LEADing?')      
   
                @pulseTransitionLead.setter
                def pulseTransitionLead(self,value:int):
                        if value!=self._pulseTransitionLead:
                                self._pulseTransitionLead=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:TRANsition:LEADing {value}')      
                @property
                def pulseTransitionTrail(self):
                        return self._awg.query(f'SOURce{self._channel}:PULSe:TRANsition:TRAiling?')      
   
                @pulseTransitionTrail.setter
                def pulseTransitionTrail(self,value:int):
                        if value!=self._pulseTransitionTrail:
                                self._pulseTransitionTrail=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:TRANsition:TRAiling {value}')      
                @property
                def pulseWidth(self):
                        return self._awg.query(f'SOURce{self._channel}:PULSe:WIDTh?')   
                @pulseWidth.setter
                def pulseWidth(self,value:int):
                        if value!=self._pulseWidth:
                                self._pulseWidth=value
                                self._awg.write(f'SOURCE{self._channel}:PULSe:WIDTh {value}')      

                #### Double Pulse #########################################################################

                @property
                def doublePulseAmplitude(self):
                        return  self._awg.query(f'SOURce{self._channel}:DOUBLEPULSe:PULSe1:AMPLitude?'), self._awg.query(f'SOURce{self._channel}:DOUBLEPULSe:PULSe2:AMPLitude?')      

                @doublePulseAmplitude.setter
                def doublePulseDutyCycle(self,value:float, pulse:int):
                        if pulse==1:
                                if value!=self._doublePulseAmplitude1:
                                        self._doublePulseAmplitude1=value
                                        self._awg.write(f'SOURCE{self._channel}:DOUBLEPULSe:PULSe{pulse}:AMPLitude {value}')   
                        elif pulse==2:
                                if value!=self._doublePulseAmplitude2:
                                        self._doublePulseAmplitude2=value
                                        self._awg.write(f'SOURCE{self._channel}:DOUBLEPULSe:PULSe{pulse}:AMPLitude {value}')                         
                @property
                def doublePulseDutyCycle(self):
                        return self._awg.query(f'SOURce{self._channel}:doublePulse:DCYCle?')      

                @doublePulseDutyCycle.setter
                def doublePulseDutyCycle(self,value:float, pulse:int):
                        if value!=self._doublePulseDutyCycle:
                                self._doublePulseDutyCycle=value
                                self._awg.write(f'SOURCE{self._channel}:doublePulse:DCYCle {value}')   
                @property
                def doublePulsePeriod(self):
                        return self._awg.query(f'SOURce{self._channel}:doublePulse:PERiod?')      

                @doublePulsePeriod.setter
                def doublePulsePeriod(self,value:float, pulse:int):
                        if value!=self._doublePulsePeriod:
                                self._doublePulsePeriod=value
                                self._awg.write(f'SOURCE{self._channel}:doublePulse:PERiod {value}')     
                @property
                def doublePulseTransitionLead(self):
                        return self._awg.query(f'SOURce{self._channel}:doublePulse:TRANsition:LEADing?')      
   
                @doublePulseTransitionLead.setter
                def doublePulseTransitionLead(self,value:float, pulse:int):
                        if value!=self._doublePulseTransitionLead:
                                self._doublePulseTransitionLead=value
                                self._awg.write(f'SOURCE{self._channel}:doublePulse:TRANsition:LEADing {value}')      
                @property
                def doublePulseTransitionTrail(self):
                        return self._awg.query(f'SOURce{self._channel}:doublePulse:TRANsition:TRAiling?')      
   
                @doublePulseTransitionTrail.setter
                def doublePulseTransitionTrail(self,value:float, pulse:int):
                        if value!=self._doublePulseTransitionTrail:
                                self._doublePulseTransitionTrail=value
                                self._awg.write(f'SOURCE{self._channel}:doublePulse:TRANsition:TRAiling {value}')      
                @property
                def doublePulseWidth(self):
                        return self._awg.query(f'SOURce{self._channel}:doublePulse:WIDTh?')   
                @doublePulseWidth.setter
                def doublePulseWidth(self,value:float, pulse:int):
                        if value!=self._doublePulseWidth:
                                self._doublePulseWidth=value
                                self._awg.write(f'SOURCE{self._channel}:doublePulse:WIDTh {value}')      

                #### Burst ################################################################################     
                @property
                def burstMode(self):
                        return self._awg.query(f'SOURce{self._channel}:BURSt:MODE?')  
                @burstMode.setter
                def burstMode(self,value:int):
                        if value!=self._burstMode:
                                self._burstMode=value
                                self._awg.write(f'SOURCE{self._channel}:BURSt:MODE {value}')     
                @property
                def burstNcycles(self):
                        return self._awg.query(f'SOURce{self._channel}:BURSt:NCYCles?')  
                @burstNcycles.setter
                def burstNcycles(self,value:int):
                        if value!=self._burstNcycles:
                                self._burstNcycles=value
                                self._awg.write(f'SOURCE{self._channel}:BURSt:NCYCles {value}')     
                @property
                def burstState(self):
                        return self._awg.query(f'SOURce{self._channel}:BURSt:STATe?')  
                @burstMode.setter
                def burstState(self,value:int):
                        if value!=self._burstState:
                                self._burstState=value
                                self._awg.write(f'SOURCE{self._channel}:BURSt:STATe {value}')     


                def triggerConfig():
                        """ 
                        Configures trigger \n
                        Parameters
                        ------------
                        float:dutyCycle
                                        sets the duty cycle of the pulse waveform in %
                        float:period
                                        sets the period for the pulse waveform in seconds
                        float:transitionLead
                                        sets the rising edge time of the pulse waveform in seconds
                        float:transitionTrail
                                        sets the falling edge time of the pulse waveform in seconds
                        """                   

                def pulseConfig(self,dutyCycle:float,period:float,transitionLead:float,transitionTrail:float):
                        """ 
                        Configures pulse   \n 
                        Parameters
                        ------------
                        dutyCycle
                                Sets the duty cycle of the pulse waveform in %
                        period
                                Sets the period for the pulse waveform in seconds
                        transitionLead    
                                Sets the rising edge time of the pulse waveform in seconds
                        transitionTrail   
                                Sets the falling edge time of the pulse waveform in seconds
                        """
                        self.pulseDutyCycle=dutyCycle
                        self.pulsePeriod=period
                        self.pulseTransitionLead=transitionLead
                        self.pulseTransitionTrail=transitionTrail