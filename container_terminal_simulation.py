import simpy
import random

AVG_ARRIVAL_INTERVAL = 5 * 60 
CONTAINERS_PER_VESSEL = 150
CRANE_MOVE_TIME = 3  
TRUCK_DELIVERY_TIME = 3  
TRUCK_CYCLE_TIME = 6  

class ContainerTerminal:
    def __init__(self, env):
        self.env = env
        self.berths = simpy.Resource(env, capacity=2)
        self.cranes = simpy.Resource(env, capacity=2)
        self.trucks = simpy.Resource(env, capacity=3)
        
        self.crane_queue = simpy.Store(env, capacity=2)  
        self.truck_queue = simpy.Store(env, capacity=3)  

        for crane_id in range(1, 3):
            self.crane_queue.put(crane_id)

        for truck_id in range(1, 4):
            self.truck_queue.put(truck_id)

    def handle_vessel(self, vessel_id):

        print(f'Vessel {vessel_id} arriving at {self.env.now}')
        
        with self.berths.request() as req:
            yield req
            print(f'Vessel {vessel_id} berthed at {self.env.now}')

        
            crane_id = yield self.crane_queue.get()
            print(f'Crane {crane_id} assigned to vessel {vessel_id} at {self.env.now}')

            for container_id in range(1, CONTAINERS_PER_VESSEL+1):
                yield self.env.process(self.move_container(vessel_id, crane_id, container_id))

            self.crane_queue.put(crane_id)
            print(f'Vessel {vessel_id} leaving at {self.env.now}')

    def move_container(self, vessel_id, crane_id, container_id):
        with self.cranes.request() as crane_req:
            yield crane_req
            yield self.env.timeout(CRANE_MOVE_TIME)
            print(f'Crane {crane_id} moved container {container_id} from vessel {vessel_id} at {self.env.now}')

        truck_id = yield self.truck_queue.get()
        print(f'Truck {truck_id} assigned to move container {container_id} for vessel {vessel_id} at {self.env.now}')

        yield self.env.timeout(TRUCK_DELIVERY_TIME)
        print(f'Truck {truck_id} delivered container {container_id} for vessel {vessel_id} at {self.env.now}')
        
        yield self.env.timeout(TRUCK_DELIVERY_TIME)
        print(f'Truck {truck_id} returned after delivering container {container_id} for vessel {vessel_id} at {self.env.now}')

        self.truck_queue.put(truck_id)

def vessel_generator(env, terminal):
    vessel_id = 1
    env.process(terminal.handle_vessel(vessel_id))
    vessel_id += 1
    while True:
        yield env.timeout(random.expovariate(1.0 / AVG_ARRIVAL_INTERVAL))
        env.process(terminal.handle_vessel(vessel_id))
        vessel_id += 1

t = int(input("Enter the simulation time in hours: "))       
SIMULATION_TIME = t * 60

env = simpy.Environment()
terminal = ContainerTerminal(env)
env.process(vessel_generator(env, terminal))
env.run(until=SIMULATION_TIME)
