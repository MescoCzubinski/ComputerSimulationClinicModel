import scipy
import numpy as np
import distributions

def int_to_time_str(int_val):
    h = int_val // 100
    m = int_val % 100
    return f"{h}:{m:02d}"

random_patients = [
    (
        int_to_time_str(int(np.random.choice(distributions.enter_time_dist))),
        int(np.random.choice(distributions.registration_duration_dist)),
        int(np.random.choice(distributions.appointment_duration_dist))
    )
    for _ in range(100)
]

def main():
    for patient in random_patients:
        print(f"Arrival Time: {patient[0]}, Registration Duration: {patient[1]} mins, Appointment Duration: {patient[2]} mins")

if __name__ == "__main__":
    main()