'''
Follows the work presented in Meisheri et. al. This script will simulate
the warehouse and store, i.e. the final part of the supply chain.

'''

import numpy as np
import os
import pandas as pd

from pathlib import Path


class warehouse_store(object):

    def __init__(self):
        '''
        Define certain parameters for the problem such as
        1. number of timesteps and total simulation duration.
        2. states and action spaces.
        3. total weight and volume that can be carried by the supplier (truck)
           this should be less than the average sales volume and weight.
        '''
        self.simulation_duration = 8#1388 (1396-8)
        self.states = None
        self.action = None
        self.weight_capacity = 1000 ## DOUBLE CHECK
        self.volume_capacity = 1000 ## DOUBLE CHECK
        self.products_metadata = None
        self.forecast_data = None

    def initialize(self, metadata, forecast_data):
        '''
        Reads data files; initializes states and actions.
        '''
        self.products_metadata = pd.read_excel(metadata,sheet_name="50_products")
        self.forecast_data = pd.read_excel(forecast_data,sheet_name="50_products")
        num_products = self.products_metadata.shape[0]
        ## Immediate forecasts include the forecasts for the next 2 days.
        immediate_forecasts = self.forecast_data.iloc[0:2,2:].to_numpy().T
        current_inventory = 10*np.ones([num_products,1])
        self.states = np.hstack((current_inventory,
                        immediate_forecasts,
                        self.products_metadata['unit_volume'].to_numpy().reshape(num_products,1),
                        self.products_metadata['unit_weight'].to_numpy().reshape(num_products,1),
                        self.products_metadata['shelf_life'].to_numpy().reshape(num_products,1)))
        ## Initial action is random
        self.action = np.random.randint(0,5,(num_products,1))
        return None

    def simulate(self, metadata, forecast_data):
        '''
        Keeps track of inventory and constraints.
        Sign conventions:
            1. Removing items from warehouse = Negative
            2. Adding items to warehouse = Positive
        '''
        ##TODO: Maintain stock of inventory.
        ##TODO: Check when product will expire with shelf life.
        ##TODO: If stock reaches 0, make sure you can't sell that product.
        self.initialize(metadata, forecast_data)
        curr_timestep = 0
        while curr_timestep <= self.simulation_duration:
            self.states[:,0,None] -= self.action
            print("Time step = ",curr_timestep)
            print(self.states[:,1:3])
            self.bookkeep(curr_timestep)
            curr_timestep += 1
            ## TODO: Replenish stock at certain intervals.
            ## TODO: Update forecast to have next two days of expected sales.
        # print(self.states)
        return None

    def bookkeep(self, timestep):
        '''
        Update forecasts and remove expired products from inventory.
        '''
        # initial_forecast = forecast_data.iloc[0:2,2:].to_numpy().T
        next_timestamp = int(np.floor(timestep/4))
        self.states[:,1:3] = self.forecast_data.iloc[next_timestamp:next_timestamp+2,2:].to_numpy().T
        return None


if __name__ == "__main__":
   metadata_file = Path(os.path.dirname(os.getcwd())+"/data/instacart-market-basket-analysis/products_metadata.xlsx")
   forecast_data = Path(os.path.dirname(os.getcwd())+"/data/instacart-market-basket-analysis/scenarios.xlsx")
   w = warehouse_store()
   w.simulate(metadata_file, forecast_data)