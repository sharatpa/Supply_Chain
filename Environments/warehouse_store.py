'''
Follows the work presented in Meisheri et. al. This script will simulate
the warehouse and store, i.e. the final part of the supply chain.

Author: Sharat Chidambaran
'''

import numpy as np
import os

class warehouse(object):

    def __init__(self):
        ## Update once a day.
        self.timestep = 1
        self.states = None
        self.action_space = None
        self.max_capacity = 0

    def initialize(self, data):
        ## Initialize the actions.
        num_products = 220 # Obtained from Barat et. al.
        return None

    def get_states(self):
        return None

if __name__ == "__main__":
   data_directory = os.path.dirname(os.getcwd())+"/data/instacart-market-basket-analysis"
   print(data_directory)
   w = warehouse_store()