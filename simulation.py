""""
Moduł symulujący działanie przychodni medycznej z rejestracją i gabinetami lekarskimi.
"""
import numpy as np
import distributions as dist


class SimulationResult:
    """Agreguje wyniki pojedynczego uruchomienia symulacji.

    Attributes:
        avg_time: Średni łączny czas spędzony w przychodni na pacjenta.
        idle_time: Łączny czas bezczynności wszystkich lekarzy.
        patient_times_total: Lista całkowitych czasów pobytu pacjentów.
        patient_times_wait: Lista czasów oczekiwania w kolejce do lekarza.
        idle_times: Lista czasów bezczynności dla każdego lekarza.
        overtime: Łączny czas pracy która przychodnia potrzebowała by na obsłużenie wszystkich po zamknięciu.
    """

    def __init__(self, avg_time, idle_time, patient_times, patient_times_wait, idle_times, overtime):
        self.avg_time = avg_time
        self.idle_time = idle_time
        self.patient_times_total = patient_times
        self.patient_times_wait = patient_times_wait
        self.idle_times = idle_times
        self.overtime = overtime


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
            # If patient arrives before clinic opens
            pre_wait = 0
            if arrival < dist.clinic_open_time:
                pre_wait = dist.clinic_open_time - arrival
                arrival = dist.clinic_open_time

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
            self.doctor_free_at[doc_idx] = end_visit + 1

            # Patient total time
            total_time = end_visit - arrival + pre_wait
            self.patient_times_total.append(total_time)
            self.patient_times_wait.append(start_visit  - end_reg + pre_wait)

        for i in range(self.num_doctors):
            if self.doctor_free_at[i] < dist.clinic_close_time:
                self.doctor_idle_time[i] += (
                    dist.clinic_close_time - self.doctor_free_at[i]
                )
        
        last_finish_time = max(self.doctor_free_at)
        overtime = last_finish_time - dist.clinic_close_time 

        avg_patient_time = np.mean(self.patient_times_total)
        total_idle_time = np.sum(self.doctor_idle_time)

        return SimulationResult(
            avg_patient_time,
            total_idle_time,
            self.patient_times_total,
            self.patient_times_wait,
            self.doctor_idle_time.tolist(),
            overtime
        )


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
        patients = dist.get_scheduled_patients(patients, num_doctors)

    sim = ClinicSimulation(num_registration_desks, num_doctors, patients)
    return sim.run()


def run_walk_in_simulation(num_registration_desks=2, num_doctors=3, patients=100):
    """Uruchamia symulację dla pacjentów bez umówionego terminu.

    Args:
        num_registration_desks: Liczba okienek rejestracji.
        num_doctors: Liczba gabinetów/lekarzy.
        patients: Liczba pacjentów lub gotowa lista .

    Returns:
        SimulationResult: Wyniki symulacji.
    """
    if not isinstance(patients, list):
        patients = dist.get_run_walk_in_patients(patients)

    sim = ClinicSimulation(num_registration_desks, num_doctors, patients)
    return sim.run()
