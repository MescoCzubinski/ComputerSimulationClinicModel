import numpy as np
import matplotlib.pyplot as plt

# we can combine both times
average_appointment_duration = 17
appointment_reserved_time = 20

clinic_open_time = 0
clinic_close_time = 600 # 10 hours in minutes

scheduled_registration_time_multiplier = 1.0
run_walk_in_registration_time_multiplier = 1.5 # walk-in patients take longer at registration

def get_walk_in_arrival_time_dist(num_patients):
    first_pic = 120
    second_pic = 420
    dist_first_pic = np.random.normal(loc=first_pic, scale=120, size=num_patients)
    dist_second_pic = np.random.normal(loc=second_pic, scale=120, size=num_patients)
    combined_dist = np.concatenate([dist_first_pic, dist_second_pic])
    return combined_dist[(combined_dist >= clinic_open_time) & (combined_dist <= clinic_close_time)]

def get_scheduled_arrival_time_dist(num_patients, num_doctors):
    avg_space_time = max(clinic_close_time // (num_patients // num_doctors), appointment_reserved_time)

    appointment_times = []
    for i in range(num_patients):
        appointment_times.append((i // num_doctors) * avg_space_time)
    return appointment_times

def get_registration_duration_dist(num_patients, multiplier):
    return (np.random.exponential(scale=1.0, size=num_patients) * multiplier) + 1 # minimum 1 minute

def get_appointment_duration_dist(num_patients):
    return np.random.gamma(shape=average_appointment_duration, scale=1, size=num_patients) + 1 # minimum 1 minute

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
            int(np.random.choice(get_walk_in_arrival_time_dist(num_patients))),
            int(np.random.choice(get_registration_duration_dist(num_patients, run_walk_in_registration_time_multiplier))),
            int(np.random.choice(get_appointment_duration_dist(num_patients)))
        )
        for _ in range(num_patients)
    ]

    patients.sort(key=lambda x: x[0])
    
    return patients

# max patients per doctor
# print(get_scheduled_patients(90, 3))
# print(get_run_walk_in_patients(90))

# avg pacients per doctor
# print(get_scheduled_patients(50, 3))
# print(get_run_walk_in_patients(50))

# appointment duration distribution plot
# plt.hist(get_appointment_duration_dist(1000), bins=50, density=True)
# plt.show()

# walk-in arrival time distribution plot
# plt.hist(get_walk_in_arrival_time_dist(1000), bins=50, density=True)
# plt.show()

# registration duration distribution plot
# plt.hist(get_registration_duration_dist(1000, 1), bins=50, density=True)
# plt.show()