import simulation as sim

def list_pprint(lst):
    """
    Funkcja pomocnicza do czytelnego wypisywania liczb.
    Args:
        lst (list): Lista liczb do wypisania.
    """
    print(list(map(float, lst)))

def main():
    """Wyświetla wyniki symulacji przychodni z terminami i bez."""
    scheduled_result = sim.run_scheduled_simulation(3, 10, 300)
    walk_in_result = sim.run_walk_in_simulation(3, 10, 300)

    print("Z umawianym terminem:")
    print(scheduled_result.idle_times, scheduled_result.avg_time)
    
    print("\nBez umawiania terminu:")
    print(walk_in_result.idle_times, walk_in_result.avg_time)

    list_pprint(walk_in_result.patient_times_wait)

if __name__ == "__main__":
    main()
