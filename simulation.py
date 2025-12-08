""""
Moduł symulujący działanie przychodni medycznej z rejestracją i gabinetami lekarskimi.
"""
import numpy as np
import distributions


class SimulationResult:
    """Agreguje wyniki pojedynczego uruchomienia symulacji.

    Attributes:
        avg_time: Średni łączny czas spędzony w przychodni na pacjenta.
        idle_time: Łączny czas bezczynności wszystkich lekarzy.
        patient_times_total: Lista całkowitych czasów pobytu pacjentów.
        patient_times_wait: Lista czasów oczekiwania w kolejce do lekarza.
        idle_times: Lista czasów bezczynności dla każdego lekarza.
    """

    def __init__(self, avg_time, idle_time, patient_times, patient_times_wait, idle_times):
        self.avg_time = avg_time                        # avg patient wait time (total visit)
        self.idle_time = idle_time                      # combined doctors idle time
        self.patient_times_total = patient_times        # patient wait times (total visit)
        self.patient_times_wait = patient_times_wait    # patient wait times (for appointment)
        self.idle_times = idle_times                    # doctor idle times


class ClinicSimulation:
    """Symuluje pracę przychodni dla zadanej liczby rejestracji i gabinetów."""

    def __init__(self, num_registration_desks, num_doctors, patients):
        """Inicjalizuje kolejki pacjentów oraz zmienne zbiorcze.

        Attributes:
            num_registration_desks: Liczba okienek rejestracji.
            num_doctors: Liczba gabinetów/lekarzy.
            patients: Lista krotek (czas przyjścia, czas rejestracji, czas wizyty).
            registration_free_at: stany okienek rejestracji.
            doctor_free_at: stany gabinetów lekarskich.
            doctor_idle_time: Czasy bezczynności poszczególnych lekarzy.
            patient_times_total: Lista całkowitych czasów pobytu pacjentów.
            patient_times_wait: Lista czasów oczekiwania w kolejce do lekarza.

        Args:
            num_registration_desks: Liczba okienek rejestracji.
            num_doctors: Liczba gabinetów/lekarzy.
            patients: Lista krotek (czas przyjścia, czas rejestracji, czas wizyty).
        """
        self.num_registration_desks = num_registration_desks
        self.num_doctors = num_doctors
        self.patients = sorted(patients, key=lambda x: x[0])
        self.registration_free_at = np.zeros(num_registration_desks)
        self.doctor_free_at = np.zeros(num_doctors)
        self.doctor_idle_time = np.zeros(num_doctors)
        self.patient_times_total = []
        self.patient_times_wait = []


    def run(self):
        """Uruchamia symulację przepływu wszystkich pacjentów.

        W każdej iteracji pacjent zajmuje pierwsze wolne okienko rejestracji,
        następnie czeka na wolnego lekarza. Czas bezczynności lekarzy jest
        kumulowany, a dla każdego pacjenta zapisywany jest czas całkowity i
        czas oczekiwania na wizytę.

        Returns:
            SimulationResult: Agregat metryk z pojedynczego przebiegu.
        """
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
            self.patient_times_total.append(total_time)
            self.patient_times_wait.append(start_visit  - end_reg)


        avg_patient_time = np.mean(self.patient_times_total)
        total_idle_time = np.sum(self.doctor_idle_time)

        return SimulationResult(avg_patient_time, total_idle_time, self.patient_times_total, self.patient_times_wait, self.doctor_idle_time.tolist())


def run_scheduled_simulation(num_registration_desks=2, num_doctors=3, patients=100):
    """Uruchamia symulację dla pacjentów z umówionym terminem.

    Args:
        num_registration_desks: Liczba okienek rejestracji.
        num_doctors: Liczba gabinetów/lekarzy.
        patients: Liczba pacjentów lub gotowa lista .

    Returns:
        SimulationResult: Wyniki symulacji.
    """
    if not isinstance(patients, list):
        patients = distributions.get_scheduled_patients(patients, num_doctors)

    sim = ClinicSimulation(num_registration_desks, num_doctors, patients)
    return sim.run()


def run_walk_in_simulation(num_registration_desks=2, num_doctors=3, patients=100):
    """Uruchamia symulację dla pacjentów przychodzących bez zapisu.

    Args:
        num_registration_desks: Liczba okienek rejestracji.
        num_doctors: Liczba gabinetów/lekarzy.
        num_patients: Liczba pacjentów.

    Returns:
        SimulationResult: Wyniki symulacji.
    """
    if not isinstance(patients, list):
        patients = distributions.get_run_walk_in_patients(patients)

    sim = ClinicSimulation(num_registration_desks, num_doctors, patients)
    return sim.run()
