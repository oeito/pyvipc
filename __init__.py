import pyvisa
import numpy as np






class ArbRiderAWG:
        def __init__(self,resource_name:str):
                try:
                        rm=pyvisa.ResourceManager('@py')
                        self.resource=rm.open_resource(resource_name)
                except:
                        print('Pyvisa not installed')
                        raise
                self.write("*CLS")
        
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
        
        

