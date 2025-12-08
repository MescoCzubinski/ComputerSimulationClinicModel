import simulation as sim

import numpy as np
import matplotlib.pyplot as plt
import simulation as sim


def run_multiple_simulations(
        isScheduled=True,
        runs=50,
        num_registration_desks=2,
        num_doctors=3,
        num_patients=100,
):
    avg_times = []
    idle_total = []

    for i in range(runs):
        if isScheduled:
            result = sim.run_scheduled_simulation(num_registration_desks, num_doctors, num_patients)
        else:
            result = sim.run_walk_in_simulation(num_registration_desks, num_doctors, num_patients)

        avg_times.append(result.avg_time)
        idle_total.append(result.idle_time)
        print(str(int(i/runs * 100)) + "%")

    return {
        "avg_times": np.array(avg_times),
        "idle": np.array(idle_total)
    }


def print_stats(data, name = ""):
    print("\n==== STATYSTYKI DLA ", name, " ====")
    print("Średnia:", np.mean(data))
    print("Mediana:", np.median(data))
    print("Odchylenie std:", np.std(data))
    print("Min:", np.min(data))
    print("Max:", np.max(data))
    print("Percentyl 90%:", np.percentile(data, 90))
    print("Percentyl 95%:", np.percentile(data, 95))


import numpy as np
import matplotlib.pyplot as plt
import simulation as sim


def run_multiple_simulations(
        isScheduled=True,
        runs=50,
        num_registration_desks=2,
        num_doctors=3,
        num_patients=100,
):
    avg_times = []
    idle_total = []

    for i in range(runs):
        if isScheduled:
            result = sim.run_scheduled_simulation(num_registration_desks, num_doctors, num_patients)
        else:
            result = sim.run_walk_in_simulation(num_registration_desks, num_doctors, num_patients)

        avg_times.append(result.avg_time)
        idle_total.append(result.idle_time)
        print(str(int(i/runs * 100)) + "%")

    return {
        "avg_times": np.array(avg_times),
        "idle": np.array(idle_total)
    }


def print_stats(data, name = ""):
    print("\n==== STATYSTYKI DLA ", name, " ====")
    print("Średnia:", np.mean(data))
    print("Mediana:", np.median(data))
    print("Odchylenie std:", np.std(data))
    print("Min:", np.min(data))
    print("Max:", np.max(data))
    print("Percentyl 90%:", np.percentile(data, 90))
    print("Percentyl 95%:", np.percentile(data, 95))


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
    scheduled_result = sim.run_scheduled_simulation()
    walk_in_result = sim.run_walk_in_simulation()

    print("Z umawianym terminem:")
    print(scheduled_result.idle_times, scheduled_result.avg_time)
    
    print("\nBez umawiania terminu:")
    print(walk_in_result.idle_times, walk_in_result.avg_time)

    pprint(walk_in_result.patient_times_wait)


    print("\nZ umawianym terminem:")    

    dataS = run_multiple_simulations(True)

    print("\nBez umawianego terminu:")

    dataW = run_multiple_simulations(False)

    print("\nZ umawianym terminem:")    
    print_stats(dataS["avg_times"], "Średni czas spędzony przez pacjenta")
    print_stats(dataS["idle"], "Bezczynność gabinetów")
    
    print("\nBez umawianego terminu:")
    print_stats(dataW["avg_times"], "Średni czas spędzony przez pacjenta")
    print_stats(dataW["idle"], "Bezczynność gabinetów")


if __name__ == "__main__":
    main()
