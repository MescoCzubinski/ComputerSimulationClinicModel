import numpy as np
import matplotlib.pyplot as plt

N=1000

nine_o_clock = 900
two_o_clock = 1400
dist_nine_o_clock = np.random.normal(loc=nine_o_clock, scale=180, size=N)
dist_two_o_clock = np.random.normal(loc=two_o_clock, scale=180, size=N)
enter_time_dist = np.concatenate([dist_nine_o_clock, dist_two_o_clock])

registration_duration_dist = np.random.exponential(scale=1.0, size=N)

appointment_duration_dist = np.random.gamma(shape=2.0, scale=10.0, size=N)

def time_to_minutes(val):
    hours = int(val) // 100
    minutes = int(val) % 100
    return (hours - 9) * 60 + minutes


# plt.hist(appointment_duration_dist, bins=50, density=True)
# plt.show()

# plt.hist(enter_time_dist, bins=50, density=True)
# plt.show()

# plt.hist(registration_duration_dist, bins=50, density=True)
# plt.show()