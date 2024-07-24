import simpy
import random

AVG_ARRIVAL_INTERVAL = 5 
CONTAINERS_PER_VESSEL = 150
CRANE_MOVE_TIME = 3
TRUCK_CYCLE_TIME = 6 

class ContainerTerminal:
    def __init__(self, env):
        self.env = env
        self.berths = simpy.Resource(env, capacity=2)
        self.cranes = simpy.Resource(env, capacity=2)
        self.trucks = simpy.Resource(env, capacity=3)

    def handle_vessel(self, vessel_id):
        # Simulate vessel arrival
        print(f'Vessel {vessel_id} arriving at {self.env.now}')
        
        with self.berths.request() as req:
            yield req
            print(f'Vessel {vessel_id} berthed at {self.env.now}')

            for _ in range(CONTAINERS_PER_VESSEL):
                yield self.env.process(self.move_container(vessel_id))

            print(f'Vessel {vessel_id} leaving at {self.env.now}')

    def move_container(self, vessel_id):
        with self.cranes.request() as crane_req:
            yield crane_req
            yield self.env.timeout(CRANE_MOVE_TIME)
            print(f'Crane moved container from vessel {vessel_id} at {self.env.now}')

        with self.trucks.request() as truck_req:
            yield truck_req
            yield self.env.timeout(TRUCK_CYCLE_TIME)
            print(f'Truck transported container for vessel {vessel_id} at {self.env.now}')

def vessel_generator(env, terminal):
    vessel_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / AVG_ARRIVAL_INTERVAL))
        env.process(terminal.handle_vessel(vessel_id))
        vessel_id += 1
        
t = int(input("Enter the simulation time in hours: "))       
SIMULATION_TIME = t * 60

# Set up and start the simulation
env = simpy.Environment()
terminal = ContainerTerminal(env)
env.process(vessel_generator(env, terminal))
env.run(until=SIMULATION_TIME)