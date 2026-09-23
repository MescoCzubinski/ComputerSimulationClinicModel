import numpy as np
import matplotlib.pyplot as plt
import simulation as sim
import analysis

def run_multiple_simulations(
        isScheduled=True,
        runs=100,
        num_registration_desks=2,
        num_doctors=3,
        num_patients=85,
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
    print("Percentyl 95%:", np.percentile(data, 95))
    print("Percentyl 90%:", np.percentile(data, 90))
    print("Percentyl 10%:", np.percentile(data, 10))
    print("Percentyl 5%:", np.percentile(data, 5))


def pprint(lst):
    print(list(map(float, lst)))

def main():
    # """Wyświetla wyniki symulacji przychodni z terminami i bez."""
    # scheduled_result = sim.run_scheduled_simulation(2, 2, [(-7, 2, 18), (-3, 4, 10), (9, 2, 24), (10, 1, 12), (34, 1, 19)])
    # walk_in_result = sim.run_walk_in_simulation(2, 2, [(171, 1, 23), (259, 1, 15), (418, 1, 15), (472, 2, 19), (533, 3, 17)])

    # print("Z umawianym terminem:")
    # print(scheduled_result.idle_times, scheduled_result.avg_time)
    # pprint(scheduled_result.patient_times_total)

    # print("\nBez umawiania terminu:")
    # print(walk_in_result.idle_times, walk_in_result.avg_time)
    # pprint(walk_in_result.patient_times_total)

    # """Testy statystyczne"""
    # print("\nZ umawianym terminem:")

    # dataS = run_multiple_simulations(True, num_runs)

    # print("\nBez umawianego terminu:")

    # dataW = run_multiple_simulations(False, num_runs)

    # print("\nZ umawianym terminem:")
    # print_stats(dataS["avg_times"], "Średni czas spędzony przez pacjenta")
    # print_stats(dataS["idle"], "Bezczynność gabinetów")

    # print("\nBez umawianego terminu:")
    # print_stats(dataW["avg_times"], "Średni czas spędzony przez pacjenta")
    # print_stats(dataW["idle"], "Bezczynność gabinetów")

    analysis.run_full_analysis(
        num_runs=100,
        num_registration_desks=2,
        num_doctors=5,
        num_patients=150,
        patients_range=range(10, 310, 10),
        doctors_range=range(1, 11)
    )



if __name__ == "__main__":
    np.random.seed(42)
    main()
