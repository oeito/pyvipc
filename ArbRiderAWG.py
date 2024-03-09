import pyvisa
import numpy as np






class ArbRider:
        def __init__(self,resource_name:str):
                try:
                        rm=pyvisa.ResourceManager('@py')
                        self.resource=rm.open_resource(resource_name)
                except:
                        print('Pyvisa not installed')
                        raise
                self.write("*CLS")


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
        ## Setters #############################################

        @amplitude.setter
        def amplitude(self,value:float):
                self._amplitude
        @function.setter
        def function(self,value:str):
                self._function
        @frequency.setter
        def frequency(self,value:int):
                self._frequency
        @offset.setter
        def offset(self,value:float):
                self._offset   
        @output.setter
        def output(self,value:int):
                self._output 
        @phase.setter
        def phase(self,value:int):
                self._phase
        ## Functions #############################################

        def idn(self):
                return self.resource.query('*IDN?')
        
        def write(self, msg):
                self.resource.write(msg)

        def query(self, msg):
                return self.resource.query(msg)
        
        def close(self):
                return self.resource.close()
        
        def pulse(self,on,off):
                return 0
        
        

