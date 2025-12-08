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
    alpha = 4
    mean = -10
    std = 4
    delta = alpha / np.sqrt(1 + alpha**2)

    z0 = np.random.normal(0, 1, num_patients)
    z1 = np.random.normal(0, 1, num_patients)

    x = delta * np.abs(z0) + np.sqrt(1 - delta**2) * z1

    return mean + std * x


def get_scheduled_arrival_time_dist(num_patients, num_doctors):
    offsets = get_arrival_offset(num_patients)
    return [
        (i // num_doctors) * appointment_reserved_time + offsets[i]
        for i in range(num_patients)
    ]


def get_registration_duration_dist(num_patients, multiplier):
    return (np.random.exponential(scale=1.0, size=num_patients) * multiplier) + 1


def get_appointment_duration_dist(num_patients):
    return np.random.gamma(shape=average_appointment_duration, scale=1, size=num_patients) + 1


def get_scheduled_patients(num_patients, num_doctors):
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
