import argparse

class keyvalue(argparse.Action): 
    def __call__( self , parser, namespace, 
                 values, option_string = None): 
        setattr(namespace, self.dest, dict()) 
        for value in values: 
              key, value = value.split('=') 
              getattr(namespace, self.dest)[key] = value 


def splitString(string):
    return string.split(',')