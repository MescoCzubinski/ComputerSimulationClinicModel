import scipy
import numpy as np
import distributions
import simulation as sim

def main():
    scheduled_result = sim.run_scheduled_simulation()
    walk_in_result = sim.run_walk_in_simulation()

    print("\nZ umawianym terminem:")
    print(scheduled_result.idle_times)
    
    print("Bez umawiania terminu:")
    print(walk_in_result.idle_times)

if __name__ == "__main__":
    main()