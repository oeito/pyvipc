import pyvisa
import numpy as np






class ArbRiderAWG:
        def __init__(self,resource_name:str):
                try:
                        awg=pyvisa.ResourceManager('@py').open_resource(resource_name)
                except:
                        print('Pyvisa not installed')
                self.resource=awg
        
        def idn(self):
                return self.resource.query('*IDN?')
        
        def write(self, msg):
                self.resource.write(msg)

        def query(self, msg):
                return self.resource.query(msg)
        
