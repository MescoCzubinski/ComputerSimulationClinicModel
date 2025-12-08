"""
Moduł definiujący rozkłady statystyczne używane w symulacji.
"""
import numpy as np
import matplotlib.pyplot as plt

# we can combine both times
average_appointment_duration = 17
appointment_reserved_time = 20

clinic_open_time = 0
clinic_close_time = 600  # 10 hours in minutes

scheduled_registration_time_multiplier = 1.0
run_walk_in_registration_time_multiplier = 1.5  # walk-in patients take longer at registration


def get_walk_in_arrival_time_dist(num_patients, p_first=0.5):
    """Zwraca czasy przyjścia pacjentów bez umówionego terminu.

    Czasy są próbkowane z dwumodalnego rozkładu normalnego (piki ok. 9:00 i 14:00). 
    Wyniki są odrzucane, jeśli wypadają poza czasem pracy przychodni.

    Args:
        num_patients: Liczba pacjentów.
        p_first: Prawdopodobieństwo przypisania do pierwszej (porannej) mody.

    Returns:
        np.ndarray: Tablica minut od otwarcia przychodni dla każdego pacjenta.
    """
    mus = np.array([120, 420])
    sigmas = np.array([90, 90])

    comp_is_second = np.random.rand(num_patients) > p_first
    locs = mus[comp_is_second.astype(int)]
    scales = sigmas[comp_is_second.astype(int)]

    samples = np.random.normal(loc=locs, scale=scales)
    out_of_bounds = (samples < clinic_open_time) | (samples > clinic_close_time)
    # Rejection sample to keep the distribution shape without edge pileups.
    while np.any(out_of_bounds):
        samples[out_of_bounds] = np.random.normal(
            loc=locs[out_of_bounds],
            scale=scales[out_of_bounds],
        )
        out_of_bounds = (samples < clinic_open_time) | (samples > clinic_close_time)
    return samples


def get_arrival_offset(num_patients):
    """Generuje przesunięcia czasów przyjścia dla pacjentów umówionych.

    Zastosowano asymetryczny rozkład normalny z oczekiwaniem -10 minut,
    co pozwala odzwierciedlić tendencję pacjentów do przychodzenia przed
    czasem, z prawostronnym ogonem.

    Args:
        num_patients: Liczba pacjentów.

    Returns:
        np.ndarray: Tablica przesunięć (w minutach) względem terminu wizyty.
    """
    alpha = 4
    mean = -10
    std = 4
    delta = alpha / np.sqrt(1 + alpha**2)

    z0 = np.random.normal(0, 1, num_patients)
    z1 = np.random.normal(0, 1, num_patients)

    x = delta * np.abs(z0) + np.sqrt(1 - delta**2) * z1

    return mean + std * x


def get_scheduled_arrival_time_dist(num_patients, num_doctors):
    """Zwraca czasy przyjścia pacjentów z umówionymi wizytami.

    Wizyty rezerwowane są co 20 minut na gabinet, a każde losowanie
    otrzymuje przesunięcie wygenerowane przez `get_arrival_offset`.

    Args:
        num_patients: Liczba pacjentów.
        num_doctors: Liczba gabinetów/lekarzy.

    Returns:
        list[int]: Posortowana lista minut od otwarcia dla każdego pacjenta.
    """
    offsets = get_arrival_offset(num_patients)
    return [
        (i // num_doctors) * appointment_reserved_time + offsets[i]
        for i in range(num_patients)
    ]


def get_registration_duration_dist(num_patients, multiplier):
    """Losuje czas obsługi w rejestracji.

    Rozkład wykładniczy mnożony przez podany współczynnik pozwala
    odróżnić pacjentów umówionych od niezapowiedzianych.

    Args:
        num_patients: Liczba pacjentów.
        multiplier: Współczynnik skalujący czas rejestracji.

    Returns:
        np.ndarray: Tablica czasów rejestracji w minutach.
    """
    return (np.random.exponential(scale=1.0, size=num_patients) * multiplier) + 1


def get_appointment_duration_dist(num_patients):
    """Losuje czas wizyty lekarskiej z rozkładu gamma.

    Args:
        num_patients: Liczba pacjentów.

    Returns:
        np.ndarray: Tablica czasów trwania wizyt w minutach.
    """
    return np.random.gamma(shape=average_appointment_duration, scale=1, size=num_patients) + 1


def get_scheduled_patients(num_patients, num_doctors):
    """Buduje listę pacjentów z umówionym terminem.

    Zwraca krotki z czasem przyjścia, czasem rejestracji i czasem wizyty,
    posortowane po przybyciu.

    Args:
        num_patients: Liczba pacjentów.
        num_doctors: Liczba gabinetów/lekarzy.

    Returns:
        list[tuple[int, int, int]]: Posortowana lista parametrów pacjentów.
    """
    arrivals = get_scheduled_arrival_time_dist(num_patients, num_doctors)
    registrations = get_registration_duration_dist(num_patients, scheduled_registration_time_multiplier)
    appointments = get_appointment_duration_dist(num_patients)

    patients = [
        (int(arrivals[i]), int(registrations[i]), int(appointments[i]))
        for i in range(num_patients)
    ]
    patients.sort(key=lambda x: x[0])

    return patients


def get_run_walk_in_patients(num_patients):
    """Buduje listę pacjentów przychodzących bez zapisu.

    Args:
        num_patients: Liczba pacjentów.

    Returns:
        list[tuple[int, int, int]]: Posortowana lista parametrów pacjentów.
    """
    arrivals = get_walk_in_arrival_time_dist(num_patients)
    registrations = get_registration_duration_dist(num_patients, run_walk_in_registration_time_multiplier)
    appointments = get_appointment_duration_dist(num_patients)

    patients = [
        (int(arrivals[i]), int(registrations[i]), int(appointments[i]))
        for i in range(num_patients)
    ]
    patients.sort(key=lambda x: x[0])

    return patients

if __name__ == "__main__":
    
    np.random.seed(42)

    sample_size = 1000000

    print("max patients per doctor case:")
    print(get_scheduled_patients(90, 3))
    print('----------------------------------------------------------')
    print(get_run_walk_in_patients(90))

    print("avg pacients per doctor case:")
    print(get_scheduled_patients(50, 3))
    print('----------------------------------------------------------')
    print(get_run_walk_in_patients(50))

    print("arrival offset distribution plot case:")
    plt.hist(get_arrival_offset(sample_size), bins=50, density=True)
    plt.show()

    print("appointment duration distribution plot case:")
    plt.hist(get_appointment_duration_dist(sample_size), bins=50, density=True)
    plt.show()

    print("walk-in arrival time distribution plot case:")  
    plt.hist(get_walk_in_arrival_time_dist(sample_size), bins=50, density=True)
    plt.show()

    print("registration duration distribution plot case:")
    plt.hist(get_registration_duration_dist(sample_size, 1), bins=50, density=True)
    plt.show()
