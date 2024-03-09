import pyvisa
import numpy as np






class ArbRider:
        def __init__(self,resource_name:str):
                try:
                        rm=pyvisa.ResourceManager('@py')
                        self.rm=rm.open_resource(resource_name)
                except:
                        print('Pyvisa not installed')
                        raise
                self.write("*CLS")
                ch1=Channel(self,1)
                ch2=Channel(self,2)

        def write(self, msg):
                self.resource.write(msg)

        def query(self, msg):
                return self.resource.query(msg)
        
        def close(self):
                return self.resource.close()

        def idn(self):
                return self.query('*IDN?')
        
        
class Channel:
        def __init__(self,arbRider:ArbRider,channel:int):
                self._awg=arbRider
                self._channel=channel


        ## Properties #############################################
                
        @property
        def amplitude(self):
                return self._awg.query(f"SOURce{self._channel}:VOLTage:AMPLitude?")
        @property
        def shape(self):
                return self._awg.query(f"SOURce{self._channel}:FUNCtion:SHAPe?")
        @property
        def frequency(self):
                return self._awg.query(f"SOURce{self._channel}:FREQuency?")
        @property
        def offset(self):
                return self._awg.query(f"SOURce{self._channel}:VOLTage:OFFSet?")
        @property
        def phase(self):
                return self._awg.query(f"SOURce{self._channel}:") 
        @property
        def output(self):
                return self._awg.query(f"OUTPut{self._channel}:STATe?")
        ## Setters #############################################

        @amplitude.setter
        def amplitude(self,value:float):
                if value != self._amplitude:
                        self._amplitude=value
                        self._awg.write(f"SOURce{self._channel}:VOLTage:LEVel {value}")
        @shape.setter
        def function(self,value:str):
                if value != self._shape:
                        self._shape=value
                        self._awg.write(f"SOURce{self._channel}:FUNCtion:SHAPe {value}")
        @frequency.setter
        def frequency(self,value:int):
                if value != self._frequency:
                        self._frequency=value
                        self._awg.write(f"SOURce{self._channel}:FREQuency:FIXed {value}")
        @offset.setter
        def offset(self,value:float):
                if value != self._offset:
                        self._offset=value
                        self._awg.write(f"SOURce{self._channel}VOLTage:LEVel:OFFSet {value}")
        @phase.setter
        def phase(self,value:float):
                self._phase=value
        @output.setter
        def output(self,value:int):
                if value!=self._output:
                        self._output=value
                        self._awg.write(f"OUTPut{self._channel}:STATe {value}")          
        ## Functions #############################################