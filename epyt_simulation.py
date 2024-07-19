from epyt import epanet
from dataclasses import dataclass
import time
import pandas as pd
import matplotlib.pyplot as plt


def timing_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()  
            result = func(*args, **kwargs)  
            end_time = time.time()  
            execution_time = end_time - start_time  
            print(f"Execution time of {func.__name__}: {execution_time:.4f} seconds")
            return result, execution_time  
        return wrapper

@dataclass
class Epyt_Network_Simulation:
    inp_file: str    

    def initialize(self):
        self.network = epanet(self.inp_file)
        self.network.openHydraulicAnalysis()
        self.network.initializeHydraulicAnalysis()    

    def set_simulation_duration(self, duration_hours: int):
        self.network.setTimeSimulationDuration(duration_hours * 3600)

    #function to get the time data series of all pipes and all nodes.
    @timing_decorator     
    def get_complet_time_series(self) -> float:    

        all_parameters = self.network.getComputedTimeSeries() 
        return all_parameters
   

   # function zo get the results of specific elements (flow in pipes or pressure in nodes).
   #now is hard coded to get the flow of the pipe pipe_n410.
    @timing_decorator   
    def get_object_results(self) -> float:
        tstep, P, F,  = 1, [], []        
        
        while (tstep>0):
            t = self.network.runHydraulicAnalysis()
            P.append(self.network.getNodePressure(self.network.getNodeIndex('n59')))            
            F.append(self.network.getLinkFlows([self.network.getLinkIndex('pipe_n410')]))
            tstep=self.network.nextHydraulicAnalysisStep()       
        
        return pd.DataFrame(F)    
              

    def close(self):
        self.network.closeHydraulicAnalysis()      
        self.network.closeNetwork()

if __name__ == "__main__":
    
    # Define duration of simulation in hours. The hydraulic time step is 5 min.
    simulation_duration = 0

    network = Epyt_Network_Simulation('inp_files\p369_Leak_dual_model.inp')
    network.initialize() 
    network.set_simulation_duration(duration_hours=simulation_duration) 
       
    # 1. Get the flow results of only one pipe.
    results_1, computing_time_1 = network.get_object_results()

     # 2. get the computing time with the function getComputedTimeSeries()    
    results_2, computing_time_2 =  network.get_complet_time_series()
    
    plt.figure(figsize=(10, 6))
    plt.plot(results_1)   
    plt.title('Epyt')     
     
    textstr = (
              f'Q virtual pipe_n410\n'
              f'simulation duration: {simulation_duration: .0f} hours\n'
              f'computing_time(1 object): {computing_time_1: .2f} seconds\n'
              f'computing_time(whole time series): {computing_time_2: .2f} seconds')

    props = dict(
            boxstyle='round',            
            alpha = 0)  
    
    plt.text(0.05, 0.7, 
            textstr, 
            fontsize=9,            
            verticalalignment='top', 
            horizontalalignment='left', 
            bbox=props, ha='left', 
            va='top', 
            transform=plt.gca().transAxes)
    
    plt.savefig('figures\One_period_simulation_epyt.jpg')
    plt.close()