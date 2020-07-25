'''
Script defining the warehouse and larger supply chain environment.

Author: Sharat Chidambaran
'''
import os
import numpy as np

class warehouse(object):

    def __init__(self):
        ## Update once a day.
        self.timestep = 1
        self.states = None

if __name__ == "__main__":
   data_directory = os.path.dirname(os.getcwd())+"/data"
   print(data_directory)
   w = warehouse()