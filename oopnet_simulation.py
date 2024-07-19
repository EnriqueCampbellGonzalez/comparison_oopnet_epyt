import oopnet as on 
from dataclasses import dataclass
from datetime import timedelta, datetime
import time
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
class OOPNET_Network_Simulation:
    inp_file: str
    network: any = None
    
    def initialize(self):
        try:        
            self.network = on.Network.read(self.inp_file)
        except Exception as e:
            print(f'Error initializing network: {e}')

    def set_simulation_duration(self, duration_hours: int):
        self.network.times.duration = timedelta(seconds=duration_hours * 3600)
    
    @timing_decorator  
    def get_results(self, only_qv: bool) -> float:

        if only_qv == True:
            self.network.report.nodes = 'NONE'
            self.network.links = 'NONE'
            self.network.reportparameter.quality = 'NO'
            self.network.reportparameter.demand = 'NO'
            self.network.reportparameter.diameter = 'NO'
            self.network.reportparameter.elevation = 'NO'
            self.network.reportparameter.ffactor = 'NO'
            self.network.reportparameter.head = 'YES'
            self.network.reportparameter.reaction = 'YES'
            self.network.reportparameter.pressure = 'NO'
            self.network.reportparameter.headloss = 'NO'
            self.network.reportparameter.setting = 'NO'
            self.network.reportparameter.velocity ='NO'
            self.network.reportparameter.flow ='YES'
            self.network.report.nodes = ([on.Junction(id='n59')])
            self.network.report.links = ([on.Pipe(id = 'pipe_n410')])
        else:
            self.network.report.nodes = 'ALL'
            self.network.report.links = 'ALL'
            self.network.reportparameter.quality = 'YES'
            self.network.reportparameter.demand = 'YES'
            self.network.reportparameter.diameter = 'YES'
            self.network.reportparameter.elevation = 'YES'
            self.network.reportparameter.ffactor = 'YES'
            self.network.reportparameter.head = 'YES'
            self.network.reportparameter.reaction = 'YES'
            self.network.reportparameter.pressure = 'YES'
            self.network.reportparameter.headloss = 'YES'
            self.network.reportparameter.setting = 'YES'
            self.network.reportparameter.velocity ='YES'
            self.network.reportparameter.flow ='YES'              

        report = self.network.run()      

        return report.flow

if __name__ == "__main__":
    
    # Define duration of simulation in hours. The hydraulic time step is 5 min.
    simulation_duration = 0

    network = OOPNET_Network_Simulation('inp_files\p369_Leak_dual_model.inp')
    network.initialize()
    network.set_simulation_duration(duration_hours=simulation_duration)

    # 1. Get the flow results of only one pipe
    results_1, computing_time_1 =  network.get_results(only_qv=True)  

    # 2. Get the results of all elements.
    results_2, computing_time_2 =  network.get_results(only_qv=False)
    
    plt.figure(figsize=(10, 6))
    plt.plot(results_1)  

    plt.figure(figsize=(10, 6))
    plt.plot(results_1)   
    plt.title('OOPNET')     
     
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
        
    plt.savefig('figures\One_period_simulation_oopnet.jpg')
    plt.close()