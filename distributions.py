import numpy as np
import matplotlib.pyplot as plt

# we can combine both times
average_appointment_duration = 17
appointment_reserved_time = 20

clinic_open_time = 0
clinic_close_time = 800

scheduled_registration_time_multiplier = 1.0
run_walk_in_registration_time_multiplier = 1.5 # walk-in patients take longer at registration

def get_walk_in_arrival_time_dist(num_patients):
    nine_o_clock = 100
    two_o_clock = 600
    dist_nine_o_clock = np.random.normal(loc=nine_o_clock, scale=120, size=num_patients)
    dist_two_o_clock = np.random.normal(loc=two_o_clock, scale=120, size=num_patients)
    combined_dist = np.concatenate([dist_nine_o_clock, dist_two_o_clock])
    return combined_dist[(combined_dist >= clinic_open_time) & (combined_dist <= clinic_close_time)]

# TODO: we can simulate real scheduled appoitnemt time (not just every 20 minutes but with some human-planned distribution)
def get_scheduled_arrival_time_dist(num_patients, num_doctors):
    appointment_times = []
    for i in range(num_patients):
        appointment_times.append((i // num_doctors) * appointment_reserved_time)
    return appointment_times

def get_registration_duration_dist(num_patients, multiplier):
    return (np.random.exponential(scale=1.0, size=num_patients) * multiplier) + 1 # minimum 1 minute

def get_appointment_duration_dist(num_patients):
    return np.random.gamma(shape=average_appointment_duration, scale=1, size=num_patients) + 1 # minimum 1 minute

def time_to_minutes(val):
    hours = int(val) // 100
    minutes = int(val) % 100
    return (hours) * 60 + minutes

def get_scheduled_patients(num_patients, num_doctors):
    patients = [
        (
            int(get_scheduled_arrival_time_dist(num_patients, num_doctors)[i]),
            int(np.random.choice(get_registration_duration_dist(num_patients, scheduled_registration_time_multiplier))),
            int(np.random.choice(get_appointment_duration_dist(num_patients)))
        )
        for i in range(num_patients)
    ]

    return patients

def get_run_walk_in_patients(num_patients):
    patients = [
        (
            int(time_to_minutes(np.random.choice(get_walk_in_arrival_time_dist(num_patients)))),
            int(np.random.choice(get_registration_duration_dist(num_patients, run_walk_in_registration_time_multiplier))),
            int(np.random.choice(get_appointment_duration_dist(num_patients)))
        )
        for _ in range(num_patients)
    ]

    patients.sort(key=lambda x: x[0])
    
    return patients

# plt.hist(get_appointment_duration_dist(100), bins=50, density=True)
# plt.show()

# plt.hist(get_walk_in_arrival_time_dist(100), bins=50, density=True)
# plt.show()

# plt.hist(get_registration_duration_dist(100, 1), bins=50, density=True)
# plt.show()