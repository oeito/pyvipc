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
        def __init__(self,awg:ArbRider,channel:int):
                self._resource=awg
                self.channel(channel)



        ## Properties #############################################
                
        @property
        def amplitude(self):
                return self._amplitude
        @property
        def function(self):
                return self._function
        @property
        def frequency(self):
                return self._frequency
        @property
        def offset(self):
                return self._offset
        @property
        def output(self):
                return self._output
        @property
        def phase(self):
                return self._phase   
        @property
        def channel(self):
                return self._channel   
        @property
        def output(self):
                return self._output   
        ## Setters #############################################

        @amplitude.setter
        def amplitude(self,value:float):
                if value != self._amplitude:
                        self._amplitude=value
                        self._resource.write()
        @function.setter
        def function(self,value:str):
                if value != self._function:
                        self._function=value
        @frequency.setter
        def frequency(self,value:int):
                self._frequency=value
        @offset.setter
        def offset(self,value:float):
                self._offset=value   
        @output.setter
        def output(self,value:int):
                self._output=value 
        @phase.setter
        def phase(self,value:float):
                self._phase=value
        @channel.setter
        def channel(self,value:float):
                self._channel=value
        @output.setter
        def output(self,value:int):
                self._output=value
        ## Functions #############################################