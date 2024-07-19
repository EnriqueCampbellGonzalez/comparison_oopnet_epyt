from epyt import epanet
from dataclasses import dataclass
import time
import pandas as pd
import matplotlib.pyplot as plt

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
    def get_complet_time_series(self) -> float:

        start_time = time.time()

        all_parameters = self.network.getComputedTimeSeries()

        end_time = time.time()
        computing_time = end_time - start_time
        print(f"Simulation completed in {computing_time: .2f} seconds")

        self.network.closeHydraulicAnalysis()

        return computing_time
   

   # function zo get the results of specific elements (flow in pipes or pressure in nodes).
   #now is hard coded to get the flow of the pipe pipe_n410.
    def get_object_results(self) -> float:

        tstep, P, F,  = 1, [], []
        start_time = time.time()
        
        while (tstep>0):
            t = self.network.runHydraulicAnalysis()
            P.append(self.network.getNodePressure(self.network.getNodeIndex('n59')))            
            F.append(self.network.getLinkFlows([self.network.getLinkIndex('pipe_n410')]))
            tstep=self.network.nextHydraulicAnalysisStep()
         
        end_time = time.time()  
        computing_time = end_time - start_time 
        print(f"Simulation completed in {computing_time: .2f} seconds")

        return pd.DataFrame(F), computing_time     
              

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
    results, computing_time_1 = network.get_object_results()

     # 2. get the computing time with the function getComputedTimeSeries()    
    computing_time_2 =  network.get_complet_time_series() 
    
    plt.figure(figsize=(10, 6))
    plt.plot(results)   
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