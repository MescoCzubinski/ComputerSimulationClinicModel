import numpy as np
import distributions

class SimulationResult:
    def __init__(self, avg_time, idle_time, patient_times, idle_times):
        self.avg_time = avg_time             # avg patient wait time (total visit)
        self.idle_time = idle_time           # combined doctors idle time
        self.patient_times = patient_times   # patient wait times (total visit)
        self.idle_times = idle_times         # doctor idle times


class ClinicSimulation:
    def __init__(self, num_registration_desks, num_doctors, patients):
        self.num_registration_desks = num_registration_desks
        self.num_doctors = num_doctors
        self.patients = sorted(patients, key=lambda x: x[0])
        self.registration_free_at = np.zeros(num_registration_desks)
        self.doctor_free_at = np.zeros(num_doctors)
        self.doctor_idle_time = np.zeros(num_doctors)
        self.patient_times = []


    def run(self):
        for arrival, reg_dur, visit_dur in self.patients:
            # Registration
            reg_idx = np.argmin(self.registration_free_at)
            start_reg = max(arrival, self.registration_free_at[reg_idx])
            end_reg = start_reg + reg_dur
            self.registration_free_at[reg_idx] = end_reg

            # Doctor
            doc_idx = np.argmin(self.doctor_free_at)

            idle = max(0, end_reg - self.doctor_free_at[doc_idx])
            self.doctor_idle_time[doc_idx] += idle

            start_visit = max(end_reg, self.doctor_free_at[doc_idx])
            end_visit = start_visit + visit_dur
            self.doctor_free_at[doc_idx] = end_visit

            # Patient total time
            total_time = end_visit - arrival
            self.patient_times.append(total_time)

        avg_patient_time = np.mean(self.patient_times)
        total_idle_time = np.sum(self.doctor_idle_time)

        return SimulationResult(avg_patient_time, total_idle_time, self.patient_times, self.doctor_idle_time.tolist())


def run_scheduled_simulation(num_registration_desks=2, num_doctors=3, num_patients=100):
    patients = distributions.get_scheduled_patients(num_patients, num_doctors)

    sim = ClinicSimulation(num_registration_desks, num_doctors, patients)
    return sim.run()


def run_walk_in_simulation(num_registration_desks=2, num_doctors=3, num_patients=100):

    patients = distributions.get_run_walk_in_patients(num_patients)

    sim = ClinicSimulation(num_registration_desks, num_doctors, patients)
    return sim.run()

