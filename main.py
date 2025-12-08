import simulation as sim

def main():
    scheduled_result = sim.run_scheduled_simulation()
    walk_in_result = sim.run_walk_in_simulation(3, 10, 300)

    print("\nZ umawianym terminem:")
    print(scheduled_result.idle_times, scheduled_result.avg_time)
    
    print("Bez umawiania terminu:")
    print(walk_in_result.idle_times, walk_in_result.avg_time)

    print(walk_in_result.patient_times_wait)

if __name__ == "__main__":
    main()