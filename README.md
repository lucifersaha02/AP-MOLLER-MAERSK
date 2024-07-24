# AP-MOLLER-MAERSK
Simulating a cointainer terminal using SimPy
### Summary of Code Functionality:

- Initialization: The ContainerTerminal class initializes resources (berths, cranes, trucks) using SimPy.
- Vessel Handling: The handle_vessel method simulates the entire process from a vessel arriving, berthing, and containers being unloaded by cranes and transported by trucks.
- Container Movement: The move_container method handles the movement of containers using cranes and trucks.
- Vessel Generation: The vessel_generator function generates vessels arriving at the terminal based on an exponential distribution.
- Simulation Execution: The environment (env) runs the simulation for a specified duration (SIMULATION_TIME).
