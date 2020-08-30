'''
Follows the work presented in Meisheri et. al. This script will simulate
the warehouse and store, i.e. the final part of the supply chain.

'''

import numpy as np
import os
import pandas as pd
import random

from pathlib import Path

from scipy.stats import gaussian_kde


class warehouse_store(object):

    def __init__(self):
        '''
        Define certain parameters for the problem such as
        1. number of timesteps and total simulation duration.
        2. states and action spaces.
        3. total weight and volume that can be carried by the supplier (truck)
            this should be less than the average sales volume and weight.
        4. variables to store data files.
        '''
        self.simulation_duration = 1392#1392 (1396-8)
        self.states = None
        self.action = None
        self.weight_capacity = 1000 ## DOUBLE CHECK
        self.volume_capacity = 1000 ## DOUBLE CHECK
        self.products_meta = None
        self.forecast_data = None
        self.num_prod = 0

    def initialize(self, metadata, forecast_data):
        '''
        Reads data files; initializes states and actions.
        '''
        self.products_meta = pd.read_excel(metadata,sheet_name="50_products")
        self.forecast_data = pd.read_excel(forecast_data,sheet_name="50_products")
        self.num_prod = self.products_meta.shape[0]
        ## Immediate forecasts include the forecasts for the next 2 days.
        immediate_forecasts = self.forecast_data.iloc[0:2,2:].to_numpy().T
        current_inventory = 10*np.ones([self.num_prod,1])
        self.states = np.hstack((current_inventory,
                        immediate_forecasts,
                        self.products_meta['unit_volume'].to_numpy().reshape(self.num_prod,1),
                        self.products_meta['unit_weight'].to_numpy().reshape(self.num_prod,1),
                        self.products_meta['shelf_life'].to_numpy().reshape(self.num_prod,1)))
        ## Initial action is random.
        self.action = np.random.randint(0,5,(self.num_prod,1))
        return None

    def simulate(self, metadata, forecast_data, reward_func, agent):
        '''
        Keeps track of inventory and constraints.
        An artificial demand is created that is a Gaussian distribution
        of the expected forecast.
        Sign conventions:
            1. Removing items from warehouse = Negative
            2. Adding items to warehouse = Positive
        '''
        self.initialize(metadata, forecast_data)
        curr_timestep = 0
        demand = self.get_demand()
        while curr_timestep < self.simulation_duration:
            self.states[:,0,None] -= demand[curr_timestep,:,None]#self.action
            ## Ensure inventory does not become less than zero.
            self.states[:,0][self.states[:,0] < 0] = 0
            self.bookkeep(curr_timestep)
            curr_timestep += 1
            ## TODO: Volume and weight constraints.
        return None
    
    def get_demand(self):
        '''
        Creates artificial demand at each time step.
        '''
        demand = np.zeros((self.simulation_duration,self.num_prod))
        forecast_data = self.forecast_data.to_numpy()
        for prod in range(2,forecast_data.shape[1]):
            prod_distr = gaussian_kde(forecast_data[:,prod].astype(np.int))
            resampled_distr = prod_distr.resample(forecast_data[:,prod].astype(np.int).shape)
            std_dev_re = int(np.std(resampled_distr))
            for timestep in range(0,self.simulation_duration,4):
                daily_dem = lambda: int(forecast_data[int(timestep/4),prod]+random.randint(0,std_dev_re))
                demand[timestep,prod-2] = daily_dem()
                demand[timestep+1,prod-2] = daily_dem()
                demand[timestep+2,prod-2] = daily_dem()
        return demand

    def bookkeep(self, timestep):
        '''
        Update forecasts and remove expired products from inventory.
        Currently, removal of "expired" products is done by removing
        20% of existing inventory at the end of the month.
        '''
        next_timestamp = int(np.floor(timestep/4))
        if timestep%4 == 0 and timestep != 0:
            next_timestamp -= 1
        self.states[:,1:3] = self.forecast_data.iloc[next_timestamp:next_timestamp+2,2:].to_numpy().T
        if timestep%120 == 0 and timestep != 0:
            self.states[:,0] = np.ceil(0.8*self.states[:,0])
        return None

if __name__ == "__main__":
   metadata_file = Path(os.path.dirname(os.getcwd())+"/data/instacart-market-basket-analysis/products_metadata.xlsx")
   forecast_data = Path(os.path.dirname(os.getcwd())+"/data/instacart-market-basket-analysis/scenarios.xlsx")
   w = warehouse_store()
   reward_func = 0
   w.simulate(metadata_file, forecast_data, reward_func, agent)