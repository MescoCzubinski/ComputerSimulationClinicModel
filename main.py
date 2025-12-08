import simulation as sim

def pprint(lst):
    print(list(map(float, lst)))

def main():
    scheduled_result = sim.run_scheduled_simulation(3, 10, 300)
    walk_in_result = sim.run_walk_in_simulation(3, 10, 300)

    print("\nZ umawianym terminem:")
    print(scheduled_result.idle_times, scheduled_result.avg_time)
    
    print("Bez umawiania terminu:")
    print(walk_in_result.idle_times, walk_in_result.avg_time)

    pprint(walk_in_result.patient_times_wait)

if __name__ == "__main__":
    main()